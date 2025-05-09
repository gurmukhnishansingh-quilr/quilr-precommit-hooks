import sys
import yaml
import jsonschema
from jsonschema import validate

# Define JSON Schema 
base_action_schema = {
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "version": { "type": ["string", "number"]},
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
  "title": "Action Schema",
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "version": { "type": ["string", "number"] },
    "code": { "type": "string" },
    "name": { "type": "string" },
    "type": {
     "type": "string",
     "enum": ["use-case"]
    },
    "actiontype": { "type": "string" },
    "config": {
      "type": "object",
      "properties": {
        "meta": {
          "type": "object",
          "properties": {
            "execution_type": { "type": "string" },
            "execution_module": { "type": "string" },
            "agent_configuration": {
              "type": "object",
              "properties": {
                "agent_instructions": { "type": "string" },
                "context_instructions": { "type": "string" },
                "tools_access": {"type": "object"},
                "output_instructions": { "type": "string" },
                "communication": { "type": "string" },
                "guardrails": {
                  "type": ["string", "array"]
                }
              },
              "required": [
                "agent_instructions",
                "context_instructions",
                "tools_access",
                "output_instructions",
                "communication",
                "guardrails"
              ]
            }
          },
          "required": ["execution_type", "execution_module", "agent_configuration"]
        }
      },
      "required": ["meta"]
    },
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
    "id",
    "version",
    "code",
    "name",
    "type",
    "actiontype",
    "config",
    "outcomes",
    "tags",
    "behavior",
    "createdon",
    "updatedon"
  ]
}
engage_agent_schema = {
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "version": { "type": ["string", "number"]},
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
    "version": { "type": ["string", "number"] },
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
                "label": { "type": ["string", "number", "boolean"] },
                "value": {
                  "type": ["string", "boolean", "number"]
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
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier"
    },
    "version": {
      "type": ["string", "number"],
      "description": "Version number"
    },
    "code": {
      "type": "string",
      "description": "Code identifier"
    },
    "name": {
      "type": "string",
      "description": "Name of the rule"
    },
    "type": {
      "type": "string",
      "enum": ["behavior", "datarisk", "devicerisk", "mfarisk", "passwordhygiene", "saasrisk"],
      "description": "Type of rule"
    },
    "createdon": {
      "type": "integer",
      "description": "Creation timestamp"
    },
    "updatedon": {
      "type": "integer",
      "description": "Last update timestamp"
    },
    "posture": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Associated posture IDs"
    },
    "browser_enabled": {
      "type": "boolean",
      "description": "Is enabled in browser"
    },
    "description": {
      "type": "string",
      "description": "Description"
    },
    "query": {
      "type": "string",
      "description": "Query string"
    },
    "config": {
      "type": "object",
      "properties": {
        "datasourcetype": {
          "type": "string",
          "enum": ["datalake"],
          "description": "Data source type"
        },
        "expression": {
          "type": "string",
          "description": "Expression for data processing"
        },
        "type": {
          "type": "string",
          "description": "Event type"
        },
        "subtype": {
          "type": "string",
          "enum": ["event"],
          "description": "Subtype of event"
        },
        "status": {
          "type": "string",
          "enum": ["open"],
          "description": "Status"
        },
        "code": {
          "type": "string",
          "description": "Rule code"
        },
        "sla": {
          "type": "string",
          "description": "SLA"
        },
        "entity": {
          "type": "string",
          "description": "Entity"
        },
        "entitytype": {
          "type": "string",
          "enum": ["user"],
          "description": "Entity type"
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Tags"
        },
        "sourceofalert": {
          "type": "string",
          "description": "Source of alert"
        },
        "template": {
          "type": "string",
          "description": "Alert template"
        },
        "artifacts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "property": { "type": "string" },
              "value": { "type": "string" },
              "artifactproperties": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "artifactValue": { "type": "string" },
                    "displayInUI": { "type": "string" }
                  },
                  "required": ["artifactValue", "displayInUI"]
                }
              }
            },
            "required": ["type", "property", "value"]
          }
        },
        "properties": {
          "type": "object",
          "properties": {
            "userId": { "type": "string" },
            "userName": { "type": "string" },
            "userMail": { "type": "string" },
            "userAccountEnabled": { "type": "string" },
            "TENANT": { "type": "string" },
            "SUBSCRIBER": { "type": "string" },
            "appName": { "type": "string" },
            "appUrl": { "type": "string" },
            "appId": { "type": "string" },
            "appCategory": { "type": "string" },
            "appDomain": { "type": "string" },
            "context_id": { "type": "string" },
            "time": { "type": "string" }
          },
          "required": [
            "userId", "userName", "userMail", "userAccountEnabled",
            "TENANT", "SUBSCRIBER", "appName", "appUrl", "appId",
            "appCategory", "appDomain", "context_id", "time"
          ]
        }
      },
      "required": [
        "datasourcetype", "expression", "type", "subtype", "status",
        "code", "sla", "entity", "entitytype", "tags",
        "sourceofalert", "template", "artifacts", "properties"
      ]
    },
    "lambda": {
      "type": "string",
      "description": "Lambda function code"
    },
    "deviceRisk": {
      "type": "object",
      "properties": {
        "deviceType": { "type": "string" },
        "riskScore": { "type": "number" },
        "details": { "type": "string" }
      },
      "required": ["deviceType", "riskScore"]
    },
    "mfaRisk": {
      "type": "object",
      "properties": {
        "mfaEnabled": { "type": "boolean" },
        "riskLevel": { "type": "string" },
        "lastMfaVerification": { "type": "string" }
      },
      "required": ["mfaEnabled"]
    },
    "passwordHygiene": {
      "type": "object",
      "properties": {
        "passwordStrength": { "type": "string" },
        "lastPasswordChange": { "type": "string" },
        "passwordReuse": { "type": "boolean" }
      },
      "required": ["passwordStrength"]
    },
    "saasRisk": {
      "type": "object",
      "properties": {
        "saasApplication": { "type": "string" },
        "riskScore": { "type": "number" },
        "complianceStatus": { "type": "string" }
      },
      "required": ["saasApplication", "riskScore"]
    }
  },
  "required": [
    "id", "version", "code", "name", "type", "createdon", "updatedon",
    "posture", "browser_enabled", "description", "query", "config", "lambda"
  ]
}
execution_module_schema = {
  "type": "object",
  "properties": {
    "criticality": {
      "type": "integer",
      "description": "Criticality level of the control"
    },
    "mode": {
      "type": "string",
      "description": "Mode of operation, e.g., monitor"
    },
    "control_name": {
      "type": "string",
      "description": "Name of the control"
    },
    "control_description": {
      "type": "string",
      "description": "Description of the control"
    },
    "posture": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Posture ID"
        }
      },
      "required": ["id"]
    },
    "behavior": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Behavior ID"
        }
      },
      "required": ["id"]
    },
    "use_case": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Use case ID"
        }
      },
      "required": ["id"]
    },
    "trigger_conditions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "operator": {
            "type": ["string", "null"]
          },
          "filter_condition": {
            "type": "object",
            "properties": {
              "attribute_type": {
                "type": "string"
              },
              "attribute_id": {
                "type": "string"
              },
              "condition": {
                "type": "string"
              },
              "value": {
                "type": "string"
              }
            },
            "required": ["attribute_type", "attribute_id", "condition", "value"]
          },
          "filter_group": {
            "type": ["null"]
          },
          "editable": {
            "type": "boolean"
          },
          "supported_operators": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "required": ["filter_condition", "operator", "editable"]
      }
    },
    "filter_group": {
      "type": "null"
    },
    "actions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string"
              }
            },
            "required": ["id"]
          },
          "name": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string"
              }
            },
            "required": ["id"]
          },
          "description": {
            "type": "string"
          },
          "meta": {
            "type": "object",
            "properties": {
              "channel": { "type": "string" },
              "engagement_type": { "type": "string" },
              "message_template": { "type": "string" },
              "execution_type": { "type": "string" },
              "execution_module": { "type": "string" },
              "browser_action": { "type": "string" },
              "prompt_frequency": { "type": "string" },
              "default_conversation_params": {
                "type": "object",
                "properties": {
                  "is_urgent": { "type": "boolean" },
                  "tone": { "type": "string" },
                  "cc_manager": { "type": "boolean" },
                  "sla": { "type": "string" },
                  "sla_duration_unit": { "type": "string" },
                  "reminder_count": { "type": "integer" },
                  "custom_message": { "type": "string" }
                }
              },
              "custom_conversation_params": { "type": "object" }
            }
          }
        },
        "required": ["type", "name", "meta"]
      }
    }
  },
  "required": [
    "criticality",
    "mode",
    "control_name",
    "control_description",
    "posture",
    "behavior",
    "use_case",
    "trigger_conditions",
    "filter_group",
    "actions"
  ]
}
template_schema = {
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Name of the message"
    },
    "type": {
      "type": "string",
      "enum": ["message"],
      "description": "Type of the message"
    },
    "channel": {
      "type": "string",
      "description": "Channel where message is sent"
    },
    "content": {
      "type": "object",
      "properties": {
        "header": {
          "type": "string",
          "description": "Header of the message"
        },
        "title": {
          "type": "string",
          "description": "Main content of the message"
        },
        "description": {
          "type": "string",
          "description": "Additional description"
        },
        "acknowledgedButtons": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "description": "Button ID"
              },
              "isPrimary": {
                "type": "boolean",
                "description": "Is this the primary button"
              },
              "name": {
                "type": "string",
                "description": "Button label"
              },
              "whitelist": {
                "type": "boolean",
                "description": "Whitelist status"
              }
            },
            "required": ["id", "isPrimary", "name", "whitelist"]
          }
        }
      },
      "required": ["header", "title", "acknowledgedButtons"]
    },
    "rendered_content_type": {
      "type": "string",
      "description": "Content type of the message",
      "enum": ["application/json"]
    },
    "is_active": {
      "type": "boolean",
      "description": "Is the message active"
    }
  },
  "required": ["name", "type", "channel", "content", "rendered_content_type", "is_active"]
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
                if filename.find("classification-config-service/action/") != -1:
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
                
                elif filename.find("classification-config-service/use-case/") != -1:
                    validate(instance=data, schema=use_case_schema)
                    print(f"✅ {filename} is valid")
                elif filename.find("classification-config-service/attributes/") != -1:
                    validate(instance=data, schema=Attributes_Schema)
                    print(f"✅ {filename} is valid")
                elif filename.find("classification-config-service/behavior/") != -1:
                    validate(instance=data, schema=Behavior_Finding_Schema)
                    print(f"✅ {filename} is valid")
                elif filename.find("quilr-playbook-service/static/execution_controls") != -1:
                    validate(instance=data, schema=execution_module_schema)
                    print(f"✅ {filename} is valid")
                elif filename.find("quilr-playbook-service/static/templates") != -1:
                    validate(instance=data, schema=template_schema)
                    print(f"✅ {filename} is valid")    
                    
                else:
                    print(f"❌ {filename} has an unknown type: {data.get('type')}")
                    sys.exit(1)                   
                    
            except jsonschema.exceptions.ValidationError as e:
                print(f"❌ {filename} failed validation:\n{e.message}")
                sys.exit(1)

if __name__ == "__main__":
    main()
