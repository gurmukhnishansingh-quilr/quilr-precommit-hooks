import sys
import yaml
import jsonschema
from jsonschema import validate

# Define JSON Schema 
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
                if data.get("type") == "use-case":
                    validate(instance=data, schema=use_case_schema)
                    print(f"✅ {filename} is valid")
                elif data.get("type") == "action" and data.get("actiontype") == "ACTP_04":
                    validate(instance=data, schema=deploy_agent_schema)
                    print(f"✅ {filename} is valid")
                elif data.get("type") == "action" and data.get("actiontype") == "ACTP_01":
                    validate(instance=data, schema=engage_agent_schema)
                    print(f"✅ {filename} is valid")
                elif data.get("type") == "action" and data.get("actiontype") == "ACTP_02":
                    validate(instance=data, schema=jit_schema)
                    print(f"✅ {filename} is valid")    
                    
            except jsonschema.exceptions.ValidationError as e:
                print(f"❌ {filename} failed validation:\n{e.message}")
                sys.exit(1)

if __name__ == "__main__":
    main()
