from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.access import DnQuery
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt, RsPathAtt
from cobra.model.infra import RtDomAtt, RtDomP, HPortS, PortBlk, RtAccPortP
import yaml
import argparse

parser = argparse.ArgumentParser(description="Display Interface Profile")
parser.add_argument('intProfName', help='interface profile name')
args = parser.parse_args()

# open yaml files
f = open('credentials.yaml', 'r')
credentials = yaml.load(f)
f.close()

apicUrl = credentials['host']
loginSession = LoginSession(apicUrl, credentials['user'], credentials['pass'])
moDir = MoDirectory(loginSession)
moDir.login()

dnQuery = DnQuery('uni/infra/accportprof-' + args.intProfName)
dnQuery.queryTarget = 'children'
#dnQuery.subtreeClassFilter = 'fvAEPg'
physMo = moDir.query(dnQuery)
for obj in physMo:
	if isinstance(obj,HPortS):
		objQuery = DnQuery(obj.dn)
		objQuery.queryTarget = 'children'
		portsMo = moDir.query(objQuery)
		for ports in portsMo:
			if isinstance(ports,PortBlk):
				print ports.fromCard + '/' + ports.fromPort + '-' + ports.toPort
	if isinstance(obj,RtAccPortP):
		print obj.dn

moDir.logout()
