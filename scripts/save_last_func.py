import os
import sys
from workflow import Workflow3

function = os.getenv("function")
serial = os.getenv("serial")
his_tag = os.getenv("his_tag")
wf = Workflow3()

his = wf.cached_data('last_func:' + his_tag, max_age=0)

if not his:
	his = []
elif his[len(his) - 1] == function:
	quit()

sys.stderr.write("\n HIS was     :     {} \n".format(type(his)))
sys.stderr.write("\n HIS length     :     {} \n".format(len(his)))

sys.stderr.write("\n Saving     :     {} \n".format(function))
his.append(function)

sys.stderr.write("\n HIS saving     :     {} \n".format(his))

data = wf.cache_data('last_func:' + his_tag, his)
sys.stderr.write("\n HIS saved     :     {} \n".format(wf.cached_data('last_func:' + his_tag, max_age=0)))