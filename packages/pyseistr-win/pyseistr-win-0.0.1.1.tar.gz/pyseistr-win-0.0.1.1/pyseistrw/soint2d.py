def soint2d(din,mask,dip,order=1,niter=100,njs=[1,1],drift=0,verb=1):
	'''
	soint2d: 2D structure-oriented interpolation (unfinished)
	
	by Yangkang Chen, 2022
	
	INPUT
	dn: model  noisy data
	dip: slope
	order:    PWD order
	eps: regularization (default:0.01);
	
	OUTPUT
	ds: filtered data 
	
	EXAMPLE
	demos/test_pyseistr_soint2d.py
	'''
	from .solvers import solver
	from .solvers import cgstep
	from .operators import allpass3_lop
	import numpy as np
	
	nw=order;
	nj1=njs[0];
	nj2=njs[1];

	[n1,n2]=din.shape;
	n12=n1*n2;
	
	mm=din;
	mm=mm.flatten(order='F');
	known=np.zeros([n12,1]);
	
	if mask  is not None:
		dd=mask.flatten(order='F');
		for ii in range(0,n12):
			known[ii] = (dd[ii] !=0) ;
			dd[ii]=0;
	else:
		for ii in range(0,n12):
			known[ii] = (mm[ii] !=0) ;
			dd[ii]=0;

	pp=dipi.flatten(order='F');
	
	dout=din

	return dout
	