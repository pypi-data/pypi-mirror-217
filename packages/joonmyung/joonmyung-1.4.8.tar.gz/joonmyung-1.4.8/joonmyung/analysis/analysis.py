from joonmyung.draw import rollout
from joonmyung.meta_data import data2path
from joonmyung.metric import targetPred
from joonmyung.log import AverageMeter
from tqdm import tqdm
from contextlib import suppress
import torch.nn.functional as F
import torch
from joonmyung.utils import to_leaf


class Analysis:
    def __init__(self, model, activate = [True, False, False], detach=True, key_name=None, num_classes = 1000
                 , cls_start=0, cls_end=1, patch_start=1, patch_end=None
                 , ks = 5
                 , amp_autocast=suppress, device="cuda"):
        # Section A. Model
        self.num_classes = num_classes
        self.key_name = key_name
        self.model = model
        self.ks = ks
        self.detach = detach


        # Section B. Attention
        self.kwargs_roll = {"cls_start" : cls_start, "cls_end" : cls_end
                            , "patch_start" : patch_start, "patch_end" : patch_end}


        # Section C. Setting
        hooks = [{"name_i": 'attn_drop', "name_o": 'decoder', "fn_f": self.attn_forward, "fn_b": self.attn_backward},
                 {"name_i": 'qkv', "name_o": 'decoder', "fn_f": self.qkv_forward, "fn_b": self.qkv_backward},
                 {"name_i": 'head', "name_o": 'decoder', "fn_f": self.head_forward, "fn_b": self.head_backward}]
        hooks = [h for h, a in zip(hooks, activate) if a]


        self.amp_autocast = amp_autocast
        self.device = device
        for name, module in self.model.named_modules():
            for hook in hooks:
                if hook["name_i"] in name and hook["name_o"] not in name:
                    module.register_forward_hook(hook["fn_f"])
                    module.register_backward_hook(hook["fn_b"])

    def attn_forward(self, module, input, output):
        # input  : 1 * (8, 3, 197, 197)
        # output : (8, 3, 197, 197)
        self.info["attn"]["f"].append(output.detach() if self.detach else output)

    def attn_backward(self, module, grad_input, grad_output):
        # input  : 1 * (8, 3, 197, 192)
        # output : (8, 3, 197, 576)
        self.info["attn"]["b"].insert(0, grad_input[0].detach() if self.detach else grad_input[0])

    def qkv_forward(self, module, input, output):
        # input  : 1 * (8, 197, 192)
        # output : (8, 197, 576)
        self.info["qkv"]["f"].append(output.detach())

    def qkv_backward(self, module, grad_input, grad_output):
        # self.info["qkv"]["b"].append(grad_input[0].detach())
       pass

    def head_forward(self, module, input, output):
        # input : 1 * (8(B), 192(D)), output : (8(B), 1000(C))
        # TP = targetPred(output.detach(), self.targets.detach(), topk=self.ks)
        TP = targetPred(to_leaf(output), to_leaf(self.targets), topk=self.ks)
        self.info["head"]["TP"] = torch.cat([self.info["head"]["TP"], TP], dim=0) if "TP" in self.info["head"].keys() else TP

    def head_backward(self, module, grad_input, grad_output):
        pass

    def resetInfo(self):
        self.info = {"attn": {"f": [], "b": []}, "qkv": {"f": [], "b": []},
                     "head": {"acc1" : AverageMeter(),
                              "acc5" : AverageMeter(),
                              "pred" : None

                              }}

    def __call__(self, samples, index=None, **kwargs):
        self.resetInfo()
        self.model.zero_grad()
        self.model.eval()

        if type(samples) == torch.Tensor:
            outputs = self.model(samples, **kwargs)
            return outputs
        else:
            for self.inputs, self.targets in tqdm(samples):
                # with self.amp_autocast():
                outputs = self.model(self.inputs)
            return False

    def anaAttn(self, attn=True, grad=False, output=None, index=None,
                head_fusion="mean", discard_ratios=[0.9], data_from="cls"
                , starts=[0], ls=None, bs=None
                , reshape=False, mean=True):

        if attn:
            attn = self.info["attn"]["f"]
        if grad:
            self.info["attn"]["b"] = []
            self.model.zero_grad()
            if index == None: index = output.max(dim=1)[1]
            index = torch.eye(self.num_classes, device=self.device)[index]
            loss = (output * index).sum()
            loss.backward(retain_graph=True)
            grad = self.info["attn"]["b"]

        return rollout(attn, grad
                       , head_fusion=head_fusion, discard_ratios=discard_ratios, data_from=data_from
                       , starts=starts, ls=ls, bs=bs
                       , reshape=reshape, mean=mean)


if __name__ == '__main__':
    # Section A. Data
    dataset_name, server, device, amp_autocast = "imagenet", "148", 'cuda', torch.cuda.amp.autocast
    data_path, _ = data2path(server, dataset_name)
    data_num, batch_size = [[0, 0], [1, 0], [2, 0], [3, 0], [0, 1], [1, 1], [2, 1], [3, 1]], 16
    # data_num, batch_size = [[3, 0]], 16
    # test, activate = [False, False, True], [False, False, True]
    test, activate = [False, True], [True, False, False] # ATTN, QKV, Head

    dataset = JDataset(data_path, dataset_name, device=device)
    samples, targets, imgs, label_names = dataset.getItems(data_num)
    loader = dataset.getAllItems(batch_size)

    # Section B. Model
    # model_number, model_name = 0, "vit_small_patch16_224"
    model_number, model_name = 1, "deit_tiny_patch16_224"
    modelMaker = JModel(model_name, dataset.num_classes, model_number=model_number, device=device)
    model, args = modelMaker.getModel()
    model = Analysis(model, activate = activate, device=device)

    bs = [3]
    samples_ = samples[bs] if bs else samples
    if test[0]:
        ls, starts, col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], None, 12
        discard_ratios, head_fusion, data_from = [0.0, 0.9], "mean", "patch"  # Attention, Gradient
        output = model(samples_)
        rollout_attn = model.anaAttn(True, False, output,
                                     ls=ls, starts=starts, discard_ratios=discard_ratios,
                                     head_fusion = head_fusion, index=targets, data_from=data_from,
                                     reshape=True)

        datas = overlay(samples_, rollout_attn, dataset_name)
        drawImgPlot(datas, col=col)

    if test[1]:
        samples_.requires_grad, model.detach, k = True, False, 3
        output = model(samples_)
        attn = torch.stack(model.info["attn"]["f"], dim=1).mean(dim=[2,3])[0,-2]
        topK = attn[1:].topk(k, -1, True)[1]
        # a = torch.autograd.grad(attn.sum(), samples, retain_graph=True)[0].sum(dim=1)
        a = torch.autograd.grad(output[:,3], samples_, retain_graph=True)[0].sum(dim=1)
        b = F.interpolate(a.unsqueeze(0), scale_factor=0.05, mode='nearest')[0]
        drawHeatmap(b)
        print(1)
        # to_np(torch.stack([attn[:, :, 0], attn[:, :, 1:].sum(dim=-1)], -1)[0])


    if test[2]:
        output = model(loader)