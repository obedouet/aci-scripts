from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.access import DnQuery
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt, RsPathAtt
from cobra.model.infra import RtDomAtt, RtDomP
import yaml
import argparse

parser = argparse.ArgumentParser(description="Display Physical Domain")
parser.add_argument('physName', help='physical domain name')
parser.add_argument('-e','--epg', help='wants epg', action="store_true")
parser.add_argument('-a','--aaep', help='wants AAeP', action="store_true")
args = parser.parse_args()

# open yaml files
f = open('credentials.yaml', 'r')
credentials = yaml.load(f)
f.close()

apicUrl = credentials['host']
loginSession = LoginSession(apicUrl, credentials['user'], credentials['pass'])
moDir = MoDirectory(loginSession)
moDir.login()

dnQuery = DnQuery('uni/phys-' + args.physName)
dnQuery.queryTarget = 'children'
#dnQuery.subtreeClassFilter = 'fvAEPg'
physMo = moDir.query(dnQuery)
for obj in physMo:
    if args.epg and isinstance(obj,RtDomAtt):
	print obj.tDn
    if args.aaep and isinstance(obj,RtDomP):
	print obj.tDn

moDir.logout()
