import numpy as np
import scipy.optimize
import scipy.sparse
import scipy.sparse.linalg


def sqp(model, y, h, x0, n_iter=30, sigma=None):
    """ Solves a non-linear programming problem with equality constraints using a Gauss-Newton approximation of the Hessian

    The problem must write as follows:
    Find x that minimize: \sum (y_i - model(x)_i)^2
    subject to the constraint h(x) = 0
    
    Parameters:
    -----------
    model: callable with the signature (params, jac=False)
           must return if jac: the model evaluated at point params
                         else: the model and its jacobian under the form of a sparse matrix
           can raise ValueError in which case the model is assumed undefined at x
    y: array
       The fit data 
    h: callable with the same signature as model
    x0: array
        starting point
    n_iter: maximal number of iterations

    Returns:
    --------
    The best fit after n_iter iterations
    
    """
    n = len(x0)
    x = x0
    iter = 0
    alpha = 0.7
    
    while iter < n_iter:
        print(iter)

        val, J = model(x, jac=True)
        residuals = y - val
        if sigma is not None:
            J.data /= sigma[J.row]
            residuals /= sigma
        B = np.dot(J.T, J)
        
        gradf = -J.T * residuals
        
        if h is not None:
            cons, H = h(x, jac=True)
            M = scipy.sparse.bmat([[B, H.T], [H, None]])
            d0 = scipy.sparse.linalg.spsolve(M, -np.r_[gradf, cons])
            mu0 = d0[n:]
            d0 = d0[:n]
            obj_start = (residuals ** 2).sum() + (cons * mu0).sum()
            def phi(x):
                try:
                    if sigma is not None:
                        p = (((y - model(x)) / sigma) ** 2).sum() + (h(x) * mu0).sum()
                    else:
                        p = ((y - model(x)) ** 2).sum() + (h(x) * mu0).sum()
                except ValueError:
                    p = 1e12
                return p
        else:
            d0 = scipy.sparse.linalg.spsolve(B, -gradf)
            obj_start = (residuals ** 2).sum()
            def phi(x):
                if sigma is not None:
                    return (((y - model(x)) / sigma) ** 2).sum()
                else:
                    return ((y - model(x)) ** 2).sum()
        def crit(t):
            return phi(x + t * d0)

        t, fval, ni, funcalls = scipy.optimize.brent(crit, brack=(0, 1), full_output=True)

        dof = len(y) - len(x)
        print(('stepsize: %g, objective: %g -> %g, decrement: %g, D.o.F.: %d, objective/dof: %g' % (t, obj_start, fval, obj_start - fval, dof, fval / dof))) 
        
        x = x + t * d0
        
        iter = iter + 1
    return x





def check_cond(model, y, h, x0, sigma=None, worst=4, best=0):
    import matplotlib.pyplot as plt
    n = len(x0)
    x = x0
    iter = 0
    alpha = 0.7
    
    val, J = model(x, jac=True)
    residuals = y - val
    if sigma is not None:
        J.data /= sigma[J.row]
        residuals /= sigma
    B = np.dot(J.T, J)
        
    gradf = -J.T * residuals

    if h is not None:
        cons, H = h(x, jac=True)
        M = scipy.sparse.bmat([[B, H.T], [H, None]])
    else:
        M = B

    s, u = np.linalg.eigh(M.todense())

    print(("condition number: %g" % (abs(s).max() / abs(s).min())))
    plt.figure()
    plt.semilogy(abs(s))
    plt.ylabel('eigen values')

    plt.figure()
    reorder = np.argsort(abs(s))
    for i in range(worst):
        plt.plot(u[:,reorder[i]], label='%g' % s[reorder[i]])

    for i in range(best):
        plt.plot(u[:,-i], label='%g' % s[-i])

    plt.legend(loc='best')















