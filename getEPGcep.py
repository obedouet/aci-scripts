from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.access import DnQuery
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt, RsPathAtt, CEp
import argparse
import yaml

parser = argparse.ArgumentParser(description="Display CEp by EPG")
parser.add_argument('tenantName', help='tenant name')
parser.add_argument('apName', help='ap name')
parser.add_argument('epgName', help='EPG name')
parser.add_argument('-m', dest='macAddress', help='MAC address')
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
    if isinstance(epg,CEp):
	if (args.macAddress):
		if (args.macAddress==epg.name):
			cepQuery = DnQuery(epg.dn)
			cepQuery.queryTarget = 'children'
			cepMo = moDir.query(cepQuery)
			for cep in cepMo:
				print cep.dn
	else:
	    #print epg.name
	    cepQuery = DnQuery(epg.dn)
	    cepQuery.queryTarget = 'children'
	    cepMo = moDir.query(cepQuery)
	    for cep in cepMo:
		print epg.name + ' ' + str(cep.dn)

moDir.logout()
