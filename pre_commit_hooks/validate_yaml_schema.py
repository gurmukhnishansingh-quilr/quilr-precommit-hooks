import sys
import yaml
import jsonschema
from jsonschema import validate

# Define JSON Schema 
base_action_schema = {
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "version": { "type": "string" },
    "code": { "type": "string" },
    "name": { "type": "string" },
    "description": { "type": "string" },
    "type": { "type": "string" },
    "actiontype": { "type": "string" },
    "config": {
      "type": "object",
    },"tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "behavior": {
      "type": "array",
      "items": { "type": "string" }
    },
    "createdon": { "type": "integer" },
    "updatedon": { "type": "integer" }
  },"required": [
    "id",
    "version",
    "code",
    "name",
    "type",
    "actiontype",
    "config",
    "tags",
    "behavior",
    "createdon",
    "updatedon"]
}
use_case_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "version": {"type": "number"},
        "code": {"type": "string"},
        "name": {"type": "string"},
        "type": {"type": "string", "enum": ["use-case"]},
        "description": {"type": "string"},
        "posture": {"type": "array", "items": {"type": "string"}},
        "behavior": {"type": "array", "items": {"type": "string"}},
        "condition": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "operator": {"type": ["string", "null"]},
                    "editable": {"type": "boolean"},
                    "filter_group": {"type": ["array", "null"], "items": {"type": "object"}},
                    "filter_condition": {
                        "type": "object",
                        "properties": {
                            "attribute_type": {"type": "string"},
                            "attribute_id": {"type": "string"},
                            "condition": {"type": "string"},
                            "value": {"type": "string"},
                        },
                        "required": ["attribute_type", "attribute_id", "condition", "value"]
                    }
                },
                "required": ["filter_condition", "operator", "editable", "filter_group"]
            }
        },
        "disabled": {"type": "boolean"},
        "createdon": {"type": "integer"},
        "updatedon": {"type": "integer"}
    },
    "required": ["id", "version", "code", "name", "type", "description", "posture", "behavior", "condition", "disabled", "createdon", "updatedon"]
}
deploy_agent_schema = {
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "version": { "type": "string" },
    "code": { "type": "string" },
    "name": { "type": "string" },
    "description": { "type": "string" },
    "type": { "type": "string" },
    "actiontype": { "type": "string" },
    "config": {
      "type": "object",
      "properties": {
        "meta": {
          "type": "object",
          "properties": {
            "category": { "type": "string" },
            "info": { "type": "string" },
            "description": { "type": "string" }
          },
          "required": ["category", "info", "description"]
        },
        "execution_type": { "type": "string" },
        "execution_module": { "type": "string" },
        "agent_configuration": {
          "type": "object",
          "properties": {
            "agent_instructions": { "type": "string" }
          },
          "required": ["agent_instructions"]
        },
        "context_instructions": { "type": "string" },
        "tools_access": {
          "type": "object",
          "properties": {
            "microsoft_scheduler": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "tool": { "type": "string" },
                  "label": { "type": "string" }
                },
                "required": ["tool", "label"]
              }
            },
            "quilr": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "tool": { "type": "string" },
                  "label": { "type": "string" }
                },
                "required": ["tool", "label"]
              }
            },
            "quilr_reminder": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "tool": { "type": "string" },
                  "label": { "type": "string" }
                },
                "required": ["tool", "label"]
              }
            },
            "slack": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "tool": { "type": "string" },
                  "label": { "type": "string" }
                },
                "required": ["tool", "label"]
              }
            }
          }
        },
        "output_instructions": { "type": "string" },
        "communication": { "type": "string" },
        "guardrails": { "type": ["string", "null"] },
        "embedding": { "type": "boolean" },
        "outcomes": {
          "type": "array",
          "items": {}
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" }
        },
        "behavior": {
          "type": "array",
          "items": { "type": "string" }
        },
        "createdon": { "type": "integer" },
        "updatedon": { "type": "integer" }
      },
      "required": [
        "meta",
        "execution_type",
        "execution_module",
        "agent_configuration",
        "context_instructions",
        "tools_access",
        "output_instructions",
        "communication",
        "outcomes",
        "tags",
        "behavior",
        "createdon",
        "updatedon"
      ]
    }
  },
  "required": [
    "id",
    "version",
    "code",
    "name",
    "description",
    "type",
    "actiontype",
    "config"
  ]
}
engage_agent_schema = {
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "version": { "type": "string" },
    "code": { "type": "string" },
    "name": { "type": "string" },
    "type": { "type": "string" },
    "actiontype": { "type": "string" },
    "config": {
      "type": "object",
      "properties": {
        "meta": {
          "type": "object",
          "properties": {
            "channel": { "type": ["string", "null"] },
            "engagement_type": { "type": "string" },
            "message_template": { "type": "string" }
          },
          "required": ["engagement_type", "message_template"]
        },
        "execution_type": { "type": "string" },
        "execution_module": { "type": "string" }
      },
      "required": ["meta", "execution_type", "execution_module"]
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "behavior": {
      "type": "array",
      "items": { "type": "string" }
    },
    "outcomes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "description": { "type": "string" }
        },
        "required": ["name", "description"]
      }
    },
    "createdon": { "type": "integer" },
    "updatedon": { "type": "integer" }
  },
  "required": [
    "id",
    "version",
    "code",
    "name",
    "type",
    "actiontype",
    "config",
    "tags",
    "behavior",
    "outcomes",
    "createdon",
    "updatedon"
  ]
}
jit_schema = {
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "version": { "type": "string" },
    "code": { "type": "string" },
    "name": { "type": "string" },
    "type": { "type": "string", "enum": ["action"] },
    "actiontype": { "type": "string", "enum": ["ACTP_02"] },
    "config": {
      "type": "object",
      "properties": {
        "meta": {
          "type": "object",
          "properties": {
            "channel": { "type": ["string", "null"] },
            "engagement_type": { "type": "string", "enum": ["templatized"] },
            "message_template": { "type": "string" },
            "execution_type": { "type": "string", "enum": ["tool"] },
            "execution_module": { "type": "string", "enum": ["send_templated_user_message"] },
            "browser_action": { "type": "string" }
          },
          "required": [
            "engagement_type",
            "message_template",
            "execution_type",
            "execution_module",
            "browser_action"
          ]
        }
      },
      "required": ["meta"]
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "behavior": {
      "type": "array",
      "items": { "type": "string" }
    },
    "createdon": { "type": "integer" },
    "updatedon": { "type": "integer" }
  },
  "required": [
    "id",
    "version",
    "code",
    "name",
    "type",
    "actiontype",
    "config",
    "tags",
    "behavior",
    "createdon",
    "updatedon"
  ]
}
Attributes_Schema ={
  "type": "object",
  "required": ["id", "version", "category", "code", "tags", "type", "attributes"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid"
    },
    "version": {
      "type": "string"
    },
    "category": {
      "type": "string"
    },
    "code": {
      "type": "string"
    },
    "tags": {
      "type": ["array", "null"],
      "items": {
        "type": "string"
      }
    },
    "type": {
      "type": "string",
      "enum": ["attributes"]
    },
    "attributes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "description", "duplicate_allowed", "graph_property", "expected_datatype", "supported_operators", "id"],
        "properties": {
          "name": { "type": "string" },
          "description": { "type": "string" },
          "duplicate_allowed": { "type": "boolean" },
          "tags": {
            "type": ["array", "null"],
            "items": { "type": "string" }
          },
          "graph_property": {
            "type": ["string", "null"]
          },
          "extension_property": {
            "type": ["string", "null"]
          },
          "expected_datatype": {
            "type": "string",
            "enum": ["string", "int", "boolean", "datetime"]
          },
          "possible_values": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["label", "value", ],
              "properties": {
                "label": { "type": ["string", "int", "boolean", "number", "datetime"] },
                "value": {
                  "type": ["string", "int", "boolean", "number", "datetime"]
                },
                "tags": {
                  "type": ["array", "null"],
                  "items": { "type": "string" }
                }
              }
            }
          },
          "possible_values_query": {
            "type": ["string", "null"]
          },
          "is_searchable": {
            "type": ["boolean", "null"]
          },
          "supported_operators": {
            "type": "array",
            "items": { "type": "string" }
          },
          "id": { "type": "string" }
        }
      }
    }
  }
}
Behavior_Finding_Schema = {
  "type": "object",
  "required": ["id", "version", "code", "name", "type", "description", "query", "config", "entity", "status", "subtype"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid"
    },
    "version": {
      "type": "number"
    },
    "code": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "type": {
      "type": "string"
    },
    "createdon": {
      "type": "number"
    },
    "updatedon": {
      "type": "number"
    },
    "posture": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "browser_enabled": {
      "type": "boolean"
    },
    "description": {
      "type": "string"
    },
    "query": {
      "type": "string"
    },
    "config": {
      "type": "object",
      "required": ["expression"],
      "properties": {
        "expression": {
          "type": "string"
        }
      }
    },
    "subtype": {
      "type": "string"
    },
    "status": {
      "type": "string",
      "enum": ["open", "closed"]
    },
    "sla": {
      "type": "string"
    },
    "entity": {
      "type": "string"
    },
    "entitytype": {
      "type": "string"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "sourceofalert": {
      "type": "string"
    },
    "template": {
      "type": "string"
    },
    "artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["type", "property", "value", "artifactproperties", "artifactKey"],
        "properties": {
          "type": { "type": "string" },
          "context": { "type": "string" },
          "property": { "type": "string" },
          "value": { "type": "string" },
          "artifactKey": { "type": "string" },
          "artifactproperties": {
            "type": "object",
            "properties": {
              "artifactValue": { "type": "string" },
              "displayInUI": { "type": "string", "enum": ["enabled", "disabled"] }
            },
            "required": ["artifactValue", "displayInUI"]
          }
        }
      }
    },
    "properties": {
      "type": "object",
      "properties": {
        "userId": { "type": "string" },
        "userName": { "type": "string" },
        "userMail": { "type": "string" },
        "userAccountEnabled": { "type": ["boolean", "string"] },
        "TENANT": { "type": "string" },
        "SUBSCRIBER": { "type": "string" },
        "appName": { "type": "string" },
        "appUrl": { "type": "string" },
        "appId": { "type": "string" },
        "accountId": { "type": "string" },
        "appCategory": { "type": ["string", "array"] },
        "scope": { "type": ["string", "array"] },
        "consentBy": { "type": "string" },
        "appDomain": { "type": "string" }
      }
    },
    "lambda": {
      "type": "string"
    },
    "disabled": {
      "type": "boolean"
    }
  }
}
def main():
    for filename in sys.argv[1:]:
        with open(filename, 'r') as f:
            try:
                data = yaml.safe_load(f)
            except Exception as e:
                print(f"❌ Failed to parse {filename}: {e}")
                sys.exit(1)

            if not isinstance(data, dict):
                print(f"❌ {filename} is not a valid YAML object.")
                sys.exit(1)
            try:
                if data.get("type") == "action": 
                    validate(instance=data, schema=base_action_schema)
                    print(f"✅ {filename} is valid")
                    if data.get("type") == "action" and data.get("actiontype") == "ACTP_01":
                        validate(instance=data, schema=engage_agent_schema)
                        print(f"✅ {filename} is valid")
                    elif data.get("type") == "action" and data.get("actiontype") == "ACTP_02":
                        validate(instance=data, schema=jit_schema)
                        print(f"✅ {filename} is valid")
                    elif data.get("type") == "action" and data.get("actiontype") == "ACTP_04":
                        validate(instance=data, schema=deploy_agent_schema)
                        print(f"✅ {filename} is valid")           
                
                elif data.get("type") == "use-case":
                    validate(instance=data, schema=use_case_schema)
                    print(f"✅ {filename} is valid")
                elif data.get("type") == "attributes":
                    validate(instance=data, schema=Attributes_Schema)
                    print(f"✅ {filename} is valid")
                elif data.get("type") == "behavior":
                    validate(instance=data, schema=Behavior_Finding_Schema)
                    print(f"✅ {filename} is valid")   
                    
                else:
                    print(f"❌ {filename} has an unknown type: {data.get('type')}")
                    sys.exit(1)                   
                    
            except jsonschema.exceptions.ValidationError as e:
                print(f"❌ {filename} failed validation:\n{e.message}")
                sys.exit(1)

if __name__ == "__main__":
    main()
