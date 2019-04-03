from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.access import DnQuery
from cobra.mit.access import ClassQuery
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt, RsPathAtt
import yaml
import argparse

#parser = argparse.ArgumentParser(description="Display EPG by Ap")
#parser.add_argument('tenantName', help='tenant name')
#parser.add_argument('apName', help='ap name')
#args = parser.parse_args()

# open yaml files
f = open('credentials.yaml', 'r')
credentials = yaml.load(f)
f.close()

apicUrl = credentials['host']
loginSession = LoginSession(apicUrl, credentials['user'], credentials['pass'])
moDir = MoDirectory(loginSession)
moDir.login()

#dnQuery = DnQuery('uni/tn-' + args.tenantName + '/ap-' + args.apName)
#dnQuery.queryTarget = 'children'
#dnQuery.subtreeClassFilter = 'fvAEPg'
cQuery = ClassQuery(AEPg)
epgMo = moDir.lookupByClass(cQuery)
for epg in epgMo:
    print epg.dn

moDir.logout()
