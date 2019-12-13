import json

import conf.default as cfg
from victorops import firetovictorops, resolvetovictorops
from citadel import firetocitadel

issues = []
tickets = {}

def routing(data):
  try:
    if 'status' in data:
      status = data['status']
      name = data['alerts'][0]['labels']['alert_name']
      cluster = data['alerts'][0]['labels']['cluster_name']
      date = data['alerts'][0]['startsAt']
      if data['alerts'][0]['labels']['alert_type'] == 'event':
        msg = data['alerts'][0]['labels']['event_message']
        target = data['alerts'][0]['labels']['target_name']
        namespace = data['alerts'][0]['labels']['target_namespace']
      if data['alerts'][0]['labels']['alert_type'] == 'metric':
        msg = data['alerts'][0]['annotations']['current_value']
        target = data['alerts'][0]['labels']['pod']
        namespace = data['alerts'][0]['labels']['namespace']

      summary = cluster+" "+namespace+" "+name+" "+target
      content = "Status: "+status+"\nAlert: "+name+"\nFirst seen: "+date+"\nCluster: "+cluster+"\nNamespace: "+namespace+"\nTarget: "+name+" "+target+"\nEvent: "+msg
      issue = [date, name, target]
      str = ' '.join(issue)
      varhash = hash(str)
  
      if status == "firing":
        if str not in issues:
          issues.append(str)
          if "victorops" in cfg.channels:
            tickets[varhash] = firetovictorops(name, content, summary)
          if "citadel" in cfg.channels:
            firetocitadel(content)
        
      if status == "resolved":
        for i in issues:
          if str == i:
            issues.remove(str)
            if "victorops" in cfg.channels:
              if varhash in tickets:
                numissue = tickets[varhash]
                resolvetovictorops(numissue)
                del tickets[varhash]
            if "citadel" in cfg.channels:
              firetocitadel(content)

  except KeyError:
    print("Malformed json:", flush=True)
    print(data, flush=True) 


