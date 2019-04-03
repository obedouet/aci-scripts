from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.access import DnQuery
from cobra.model.vpc import Dom
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt, RsPathAtt
from cobra.model.pc import AggrIf
import yaml
import argparse

parser = argparse.ArgumentParser(description="Display Leafs vPC")
parser.add_argument('leafANumber', help='leaf A number')
parser.add_argument('leafBNumber', help='leaf B number')
parser.add_argument('-d','--domain', help='display vPC Domain status and details of vPC',action="store_true")
args = parser.parse_args()

# open yaml files
f = open('credentials.yaml', 'r')
credentials = yaml.load(f)
f.close()

apicUrl = credentials['host']
loginSession = LoginSession(apicUrl, credentials['user'], credentials['pass'])
moDir = MoDirectory(loginSession)
moDir.login()

if args.domain:
    nodeAQuery = DnQuery('topology/pod-1/node-' + args.leafANumber + '/sys/vpc/inst')
    nodeAQuery.queryTarget = 'children'
    nodeAMo = moDir.query(nodeAQuery)
    for vpcDomain in nodeAMo:
        if isinstance(vpcDomain,Dom):
	    print "DomainId: " + str(vpcDomain.id)
	    print "PeerState: " + vpcDomain.peerSt
	    print "Role: " + vpcDomain.operRole + ' (operational), ' + vpcDomain.oldRole + ' (configured)'
	    vpcQuery = DnQuery(vpcDomain.dn)
	    vpcQuery.queryTarget = 'children'
	    vpcMo = moDir.query(vpcQuery)
	    #for vpcIf in vpcMo:
	#	print vpcIf.name

    nodeASysQuery = DnQuery('topology/pod-1/node-' + args.leafANumber + '/sys')
    nodeASysQuery.queryTarget = 'children'
    nodeASysMo = moDir.query(nodeASysQuery)
    #for nodeObj in nodeASysMo:
    #    print nodeObj
    nodeBSysQuery = DnQuery('topology/pod-1/node-' + args.leafBNumber + '/sys')
    nodeBSysQuery.queryTarget = 'children'
    nodeBSysMo = moDir.query(nodeBSysQuery)
    #for nodeObj in nodeBSysMo:

dnQuery = DnQuery('topology/pod-1/protpaths-' + args.leafANumber + '-' + args.leafBNumber)
dnQuery.queryTarget = 'children'
#dnQuery.subtreeClassFilter = 'fvAEPg'
leafMo = moDir.query(dnQuery)
for obj in leafMo:
	#objQuery = DnQuery(obj.dn)
	#objQuery.queryTarget = 'children'
	#objMo = moDir.query(objQuery)
	#for int in objMo:
	#	print int

	if args.domain:
	    for vpcIf in vpcMo:
		if vpcIf.name == obj.name:
                    for nodeObj in nodeASysMo:
                        if isinstance(nodeObj,AggrIf):
                            if (nodeObj.name == obj.name):
                                pcIntfNodeA = nodeObj
                    for nodeObj in nodeBSysMo:
                        if isinstance(nodeObj,AggrIf):
                            if (nodeObj.name == obj.name):
                                pcIntfNodeB = nodeObj
		    print str(obj.dn) + ',\t Id:' + str(vpcIf.id) + '/' + pcIntfNodeA.id + '/' + pcIntfNodeB.id + ',\t Status:' + str(vpcIf.localOperSt) + ',\t Vlans:' + vpcIf.cfgdVlans
	else:
	    print obj.dn, obj.name
		

moDir.logout()
