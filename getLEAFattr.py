from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.access import DnQuery
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt, RsPathAtt, DomDef
from cobra.model.ethpm import PhysIf
from cobra.model.pc import AggrMbrIf, AggrIf
from cobra.model.fabric import L2IfPol
from cobra.model.l1 import RsL2IfPolCons
import yaml
import argparse

parser = argparse.ArgumentParser(description="Display Leaf")
parser.add_argument('leafNumber', help='leaf number')
parser.add_argument('-f','--full', help='display all objects', action="store_true")
args = parser.parse_args()

# open yaml files
f = open('credentials.yaml', 'r')
credentials = yaml.load(f)
f.close()

apicUrl = credentials['host']
loginSession = LoginSession(apicUrl, credentials['user'], credentials['pass'])
moDir = MoDirectory(loginSession)
moDir.login()

dnQuery = DnQuery('topology/pod-1/paths-' + args.leafNumber)
dnQuery.queryTarget = 'children'
#dnQuery.subtreeClassFilter = 'fvAEPg'
leafMo = moDir.query(dnQuery)
for obj in leafMo:
    if obj.pathT == 'leaf':
        if obj.lagT != 'node':
	    #print obj.dn
	    intfL2Pol='default'
	    intfPC=''
	    intQuery = DnQuery('topology/pod-1/node-'  + args.leafNumber + '/sys/phys-[' + obj.name + ']')
	    intQuery.queryTarget = 'children'
	    intMo = moDir.query(intQuery)
            for intAttr in intMo:
		if isinstance(intAttr, PhysIf):
		    #print obj.name, '\t',
		    if intAttr.operSt=="link-up":
			operState=intAttr.operStQual
		    else:
			operState=intAttr.operSt
		    operMode=intAttr.operMode
		    operSpeed=intAttr.operSpeed
		    operDuplex=intAttr.operDuplex
		    intfUsage=intAttr.usage
		    if intAttr.bundleIndex != "unspecified":
		        intfPC=intAttr.bundleIndex
		elif isinstance(intAttr, DomDef):
		    PhysDom=intAttr.rn
		elif isinstance(intAttr, RsL2IfPolCons):
		    intfL2Pol=intAttr.tDn
		else:
		    if args.full:
		        print intAttr
	    print obj.name, '\t', operState, '\t'+ operMode, operSpeed, operDuplex + '\t',
	    if intfUsage=="discovery":
		print
	    else:
		if intfL2Pol:
			print intfL2Pol + '\t',
		print PhysDom, '\t' + intfUsage,
		if intfPC:
			print intfPC,
		print
    else:
        print obj.name, '\t',
	intQuery = DnQuery('topology/pod-1/node-'  + args.leafNumber + '/sys/phys-[' + obj.name + ']')
	intQuery.queryTarget = 'children'
	intMo = moDir.query(intQuery)
        for intAttr in intMo:
	    if isinstance(intAttr, PhysIf):
	        print intAttr.operSt, intAttr.usage

moDir.logout()
