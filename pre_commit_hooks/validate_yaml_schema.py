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
      "description": "Unique identifier for the behavior"
    },
    "version": {
      "type": ["string", "number"],
      "description": "Version number of the behavior"
    },
    "code": {
      "type": "string",
      "description": "Code representing the behavior"
    },
    "name": {
      "type": "string",
      "description": "Name of the behavior"
    },
    "type": {
      "type": "string",
      "enum": [
        "behavior"
      ],
      "description": "Type of the configuration, should be 'behavior'"
    },
    "createdon": {
      "type": "integer",
      "description": "Timestamp of creation"
    },
    "updatedon": {
      "type": "integer",
      "description": "Timestamp of last update"
    },
    "psture": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "List of postures associated with the behavior"
    },
    "browser_enabled": {
      "type": "boolean",
      "description": "Indicates if the behavior is enabled in the browser"
    },
    "description": {
      "type": "string",
      "description": "Description of the behavior"
    },
    "query": {
      "type": "string",
      "description": "SQL query associated with the behavior"
    },
    "config": {
      "type": "object",
      "properties": {
        "datasourcetype": {
          "type": "string",
          "enum": [
            "datalake"
          ],
          "description": "Type of data source"
        },
        "expression": {
          "type": "string",
          "description": "Expression for data processing"
        },
        "type": {
          "type": "string",
          "description": "Type of event"
        },
        "subtype": {
          "type": "string",
          "enum": [
            "event"
          ],
          "description": "Subtype of event"
        },
        "status": {
          "type": "string",
          "enum": [
            "open"
          ],
          "description": "Status of the event"
        },
        "code": {
          "type": "string",
          "description": "Rule code"
        },
        "sla": {
          "type": "string",
          "description": "Service Level Agreement"
        },
        "entity": {
          "type": "string",
          "description": "Entity associated with the event"
        },
        "entitytype": {
          "type": "string",
          "enum": [
            "user"
          ],
          "description": "Type of entity"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "List of tags"
        },
        "sourceofalert": {
          "type": "string",
          "description": "Source of the alert"
        },
        "template": {
          "type": "string",
          "description": "Template for the alert message"
        },
        "artifacts": {
          "type": "string",
          "description": "Artifacts associated with the alert"
        },
        "properties": {
          "type": "string",
          "description": "Properties associated with the alert"
        }
      },
      "required": [
        "datasourcetype",
        "expression",
        "type",
        "subtype",
        "status",
        "code",
        "sla",
        "entity",
        "entitytype",
        "tags",
        "sourceofalert",
        "template",
        "artifacts",
        "properties",
        "posture"
      ]
    },
    "lambda": {
      "type": "string",
      "description": "Lambda function code"
    }
  },
  "required": [
    "id",
    "version",
    "code",
    "name",
    "type",
    "createdon",
    "updatedon",
    "psture",
    "browser_enabled",
    "description",
    "query",
    "config",
    "lambda"
  ]
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
