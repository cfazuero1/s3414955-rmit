#!/usr/bin/env python

import roslib
roslib.load_manifest("rosparam")
import rosparam
import rospkg

pkg = rospkg.RosPack()
paramlist = rosparam.load_file(pkg.get_path("gestures")+"/config/reem_motions.yaml")
for params, ns in paramlist:
    rosparam.upload_params(ns, params)
