from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.access import DnQuery
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt, RsPathAtt
import argparse
import yaml

parser = argparse.ArgumentParser(description="Lookup Static Path by EPG")
parser.add_argument('tenantName', help='tenant name')
parser.add_argument('apName', help='ap name')
parser.add_argument('epgName', help='EPG name')
args = parser.parse_args()

# open yaml files
f = open('credentials.yaml', 'r')
credentials = yaml.load(f)
f.close()

apicUrl = credentials['host']
loginSession = LoginSession(apicUrl, credentials['user'], credentials['pass'])
moDir = MoDirectory(loginSession)
moDir.login()

dnQuery = DnQuery('uni/tn-' + args.tenantName + '/ap-' + args.apName + '/epg-' + args.epgName)
dnQuery.queryTarget = 'children'
dnQuery.subtreeClassFilter = 'fvAEPg'
epgMo = moDir.query(dnQuery)
for epg in epgMo:
    #print epg.dn
    if isinstance(epg,AEPg):
	print 'AEPg'
    elif isinstance(epg,RsPathAtt):
	print str(epg.tDn) + ' ' + epg.encap + ' ' + epg.mode

moDir.logout()
