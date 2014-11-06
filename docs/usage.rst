========
Usage
========

To use gencmd in a project::

    import gencmd

Then you would like to create a SSP object to play with::

    age = 10.08   # log(age/yr)
    Z = 0.015/100 # 1pct solar metallicity
    mf = 'kroupa'
    mycluster = gencmd.SSP(age, Z, mf=mf)

Great! Now ``mycluster`` has a lot of nice methods like::

    isoc = mycluster.isoc               # The evolutionary model for the selected parameters
    stars = mycluster.populate(n=10000) # Make 10000 stars

The columns on  ´´isoc´´ and ´´stars´´ are the same and can be visualized using::
    
    print(mycluster.coldict)
