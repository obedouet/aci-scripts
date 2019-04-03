__author__ = 'keiran_harris'

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.session
import cobra.mit.request
import cobra.model.fv
import cobra.mit.naming
import yaml
import argparse
from cobra.internal.codec.xmlcodec import toXMLStr
import warnings
warnings.filterwarnings("ignore")


def get_args():
    parser = argparse.ArgumentParser(description="Configure EPG")
    parser.add_argument('epgName', help='EPG name')
    parser.add_argument('-d', dest='delete', help='delete the config', action='store_true')
    parser.add_argument('-f', dest='file', help='BD Config in YAML format')
    args = parser.parse_args()
    return args

def expand_vlan_range(vlans):
    vlans_numbers = []
    for vlan in vlans:
        vlan = str(vlan)
        if '-' in vlan:
            a, b = vlan.split('-')
            a, b = int(a), int(b)
            vlans_numbers.extend(range(a, b + 1))
        else:
            vlans_numbers.append(int(vlan))
    return vlans_numbers

# Get command line arguments
args = get_args()

# open yaml files
f = open('credentials.yaml', 'r')
credentials = yaml.load(f)
f.close()

f = open(args.file, 'r')
config = yaml.load(f)
f.close()

# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession(credentials['host'], credentials['user'], credentials['pass'], secure=False, timeout=180)
md = cobra.mit.access.MoDirectory(ls)
md.login()

tenant = 'uni/tn-' + config['tenant']
app = config['application']
phyDom = config['physical_domain']
bd_name = config['bridge_domain']
# the top level object on which operations will be made
# Confirm the dn below is for your top dn
#vlans = expand_vlan_range(config['vlans'])

#for vlan in vlans:
#epg_name= 'V' + str(vlan) + '_EPG'
epg_name= args.epgName
#bd_name = 'V' + str(vlan) +'_BD'
print tenant + '/ap-' + app + '/epg-' + epg_name
topDn = cobra.mit.naming.Dn.fromString(tenant + '/ap-' + app + '/epg-' + epg_name)
topParentDn = topDn.getParent()
topMo = md.lookupByDn(topParentDn)
fvAEPg = cobra.model.fv.AEPg(topMo, name=epg_name, descr='')
fvRsDomAtt = cobra.model.fv.RsDomAtt(fvAEPg, tDn='uni/phys-' + phyDom, instrImedcy='lazy',  resImedcy='lazy')

fvRsBd = cobra.model.fv.RsBd(fvAEPg, tnFvBDName=bd_name)

if args.delete:
    fvAEPg.delete()
# commit the generated code to APIC
print toXMLStr(topMo)
c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
md.commit(c)

