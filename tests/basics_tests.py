import unittest
import sys, os
path = os.path.dirname(os.path.abspath(__file__))
path = path[:path.rfind('/')]
sys.path.insert(0, path)
from mirtorch.linear import basics
import torch
import torch.nn.functional as F
import utils
class TestBasic(unittest.TestCase):

    def test_diag(self):
        x = torch.randn(5, 5)
        P = torch.randn(5, 5)

        diag = basics.Diag(P)
        out = diag.apply(x)

        exp = P * x
        assert(torch.allclose(out, exp, rtol=1e-3))

    def test_conv1d_apply_simple(self):
        x = torch.randn(20, 16, 50)
        weight = torch.randn(33, 16, 3)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        x, weight = x.to(device), weight.to(device)

        conv = basics.Convolve1d(x.shape, weight, device=device)
        out = conv.apply(x)

        # exp = F.conv1d(x, weight)
        x = x.permute(0,2,1).detach().cpu().numpy()
        weight = weight.permute(2,1,0).detach().cpu().numpy()
        exp = utils.conv1D(x, weight, stride=1, pad=0, dilation=0)
        exp = torch.from_numpy(exp).to(device).permute(0,2,1)
        assert(torch.allclose(out, exp, rtol=1.5e-3))

    def test_conv2d_apply_simple(self):
        x = torch.randn(1, 4, 5, 5)
        weight = torch.randn(8, 4, 3, 3)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        x, weight = x.to(device), weight.to(device)

        conv = basics.Convolve2d(x.shape, weight, device=device)
        out = conv.apply(x)

        # exp = F.conv2d(x, weight)
        x = x.permute(0,2,3,1).detach().cpu().numpy()
        weight = weight.permute(2,3,1,0).detach().cpu().numpy()
        exp = utils.conv2D(x, weight, stride=1, pad=0, dilation=0)
        exp = torch.from_numpy(exp).to(device).permute(0,3,1,2)
        assert(torch.allclose(out, exp, rtol=1e-3))

    def test_conv3d_apply_simple(self):
        x = torch.randn(20, 16, 50, 10, 20)
        weight = torch.randn(33, 16, 3, 3, 3)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        x, weight = x.to(device), weight.to(device)

        conv = basics.Convolve3d(x.shape, weight, device=device)
        out = conv.apply(x)

        exp = F.conv3d(x, weight)
        assert(torch.allclose(out, exp, rtol=1e-3))

    def test_conv1d_apply_hard(self):
        x = torch.randn(20, 16, 50)
        weight = torch.randn(33, 16, 3)
        bias = torch.randn(33)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        x, weight, bias = x.to(device), weight.to(device), bias.to(device)

        conv = basics.Convolve1d(x.shape, weight, bias=bias, stride=2, padding=1, dilation=2, device=device)
        out = conv.apply(x)

        exp = F.conv1d(x, weight, bias=bias, stride=2, padding=1, dilation=2)
        assert(torch.allclose(out, exp, rtol=1e-3))

    def test_conv2d_apply_hard(self):
        x = torch.randn(1, 4, 5, 5)
        weight = torch.randn(8, 4, 3, 3)
        bias = torch.randn(8)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        x, weight, bias = x.to(device), weight.to(device), bias.to(device)

        conv = basics.Convolve2d(x.shape, weight, bias=bias, stride=3, padding=2, dilation=2, device=device)
        out = conv.apply(x)

        exp = F.conv2d(x, weight, bias=bias, stride=3, padding=2, dilation=2)
        assert(torch.allclose(out, exp, rtol=1e-3))

    def test_conv3d_apply_hard(self):
        x = torch.randn(20, 16, 50, 10, 20)
        weight = torch.randn(33, 16, 3, 3, 3)
        bias = torch.randn(33)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        x, weight, bias = x.to(device), weight.to(device), bias.to(device)

        conv = basics.Convolve3d(x.shape, weight, bias=bias, stride=3, padding=3, dilation=4, device=device)
        out = conv.apply(x)

        exp = F.conv3d(x, weight, bias=bias, stride=3, padding=3, dilation=4)
        assert(torch.allclose(out, exp, rtol=1e-3))

    def test_conv1d_adjoint_simple(self):
        x = torch.randn(20, 16, 50)
        weight = torch.randn(33, 16, 3)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        x, weight = x.to(device), weight.to(device)

        Ax = F.conv1d(x, weight)
        conv = basics.Convolve1d(x.shape, weight, device=device)
        out = conv.adjoint(Ax)

        exp = F.conv_transpose1d(Ax, weight)
        assert(torch.allclose(out, exp, rtol=1e-3))

    def test_conv2d_adjoint_simple(self):
        x = torch.randn(1, 4, 5, 5)
        weight = torch.randn(8, 4, 3, 3)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        x, weight = x.to(device), weight.to(device)

        Ax = F.conv2d(x, weight)
        conv = basics.Convolve2d(x.shape, weight, device=device)
        out = conv.adjoint(Ax)

        exp = F.conv_transpose2d(Ax, weight)
        assert(torch.allclose(out, exp, rtol=1e-3))

    def test_conv3d_adjoint_simple(self):
        x = torch.randn(20, 16, 50, 10, 20)
        weight = torch.randn(33, 16, 3, 3, 3)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        x, weight = x.to(device), weight.to(device)

        Ax = F.conv3d(x, weight)
        conv = basics.Convolve3d(x.shape, weight, device=device)
        out = conv.adjoint(Ax)

        exp = F.conv_transpose3d(Ax, weight)
        assert(torch.allclose(out, exp, rtol=1e-3))
    
    def test_conv1d_adjoint_hard(self):
        x = torch.randn(20, 16, 50)
        weight = torch.randn(33, 16, 3)
        bias = torch.randn(16)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        x, weight, bias = x.to(device), weight.to(device), bias.to(device)

        Ax = F.conv1d(x, weight, stride=2, padding=1, dilation=2)
        conv = basics.Convolve1d(x.shape, weight, bias=bias, stride=2, padding=1, dilation=2, device=device)
        out = conv.adjoint(Ax)

        exp = F.conv_transpose1d(Ax, weight, bias=bias, stride=2, padding=1, dilation=2)
        assert(torch.allclose(out, exp, rtol=1e-3))


if __name__ == '__main__':
    # if torch.cuda.is_available():
    #     print(torch.cuda.get_device_name(0))
    unittest.main()