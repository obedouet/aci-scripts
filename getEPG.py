from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.access import DnQuery
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt, RsPathAtt
import yaml
import argparse

parser = argparse.ArgumentParser(description="Display EPG by Ap")
parser.add_argument('tenantName', help='tenant name')
parser.add_argument('apName', help='ap name')
parser.add_argument('-s', '--separe', help='ap name',action="store_true")
args = parser.parse_args()

# open yaml files
f = open('credentials.yaml', 'r')
credentials = yaml.load(f)
f.close()

apicUrl = credentials['host']
loginSession = LoginSession(apicUrl, credentials['user'], credentials['pass'])
moDir = MoDirectory(loginSession)
moDir.login()

dnQuery = DnQuery('uni/tn-' + args.tenantName + '/ap-' + args.apName)
dnQuery.queryTarget = 'children'
#dnQuery.subtreeClassFilter = 'fvAEPg'
epgMo = moDir.query(dnQuery)
for epg in epgMo:
    if args.separe:
        print args.tenantName + ' ' + args.apName + ' ' + epg.name
    else:
        print epg.dn, epg.name

moDir.logout()
