import torch
@torch.no_grad()
def power_iter(A, x0, max_iter=100, tol=1e-6, alert=True):
    '''
        Input:
            A: Linear Maps
            max_iter: maximum number of iterations
            tol: stopping tolerance
            x0: initial guess of singular vector corresponding to max singular value
        Ouput:
            v1: principal right singular vector
            sig1: spectral norm of A
    '''
    x = x0
    ratio_old = float('inf')
    for iter in range(max_iter):
        Ax = A * x
        ratio = torch.norm(Ax) / torch.norm(x)
        if torch.abs(ratio - ratio_old) / ratio < tol:
            if alert:
                print('calculation of max singular value accomplished at %d iterations' % (iter + 1))
            break
        ratio_old = ratio
        x = A.H * Ax
        x = x / torch.norm(x)
    sig1 = torch.norm(A * x) / torch.norm(x)
    if alert:
        print(f'The spectural norm is {float(sig1)}')
    return x, sig1
