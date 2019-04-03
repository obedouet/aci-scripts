from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.access import DnQuery
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt, RsPathAtt
from cobra.model.top import System
import yaml
import argparse

parser = argparse.ArgumentParser(description="Display Leaf")
parser.add_argument('leafNumber', help='leaf number')
args = parser.parse_args()

# open yaml files
f = open('credentials.yaml', 'r')
credentials = yaml.load(f)
f.close()

apicUrl = credentials['host']
loginSession = LoginSession(apicUrl, credentials['user'], credentials['pass'])
moDir = MoDirectory(loginSession)
moDir.login()

dnQuery = DnQuery('topology/pod-1/node-' + args.leafNumber)
dnQuery.queryTarget = 'children'
#dnQuery.subtreeClassFilter = 'fvAEPg'
leafMo = moDir.query(dnQuery)
for obj in leafMo:
    if isinstance(obj,System):
	print obj.name + ' ' + obj.serial + ' ' + obj.role + ' ' + obj.state + ' ' + str(obj.systemUpTime)

moDir.logout()
