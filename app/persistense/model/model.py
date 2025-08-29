# las tablas  de base de datos
#
#
#
#
#
#
#
#
# joel  modelos
#


# use visiondb;
 
// ----- phones -----
db.createCollection("phones", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["_id","brand","model_name"],
      properties: {
        _id: { bsonType: "string", description: "pk app: brand_model" },
        brand: { bsonType: "string" },
        model_name: { bsonType: "string" },
        image_path: { bsonType: ["string","null"] },
        created_at: { bsonType: ["date","null"] }
      }
    }
  }
});
db.phones.createIndex({brand: 1});
 
// ----- inferences -----
db.createCollection("inferences", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["_id","model","model_version","created_at","detections"],
      properties: {
        _id: { bsonType: "string", description: "image_id como PK" },
        brand: { bsonType: ["string","null"] },
        model_name: { bsonType: ["string","null"] },
        image_path: { bsonType: ["string","null"] },
        model: { bsonType: "string" },
        model_version: { bsonType: "string" },
        meta: { bsonType: ["object","null"] },
        created_at: { bsonType: "date" },
        detections: {
          bsonType: "array",
          minItems: 0,
          items: {
            bsonType: "object",
            required: ["class","conf","bbox"],
            properties: {
              class: { bsonType: "string" },
              conf: { bsonType: "double", minimum: 0, maximum: 1 },
              bbox: {
                bsonType: "object",
                required: ["xmin","ymin","xmax","ymax"],
                properties: {
                  xmin: { bsonType: "int" },
                  ymin: { bsonType: "int" },
                  xmax: { bsonType: "int" },
                  ymax: { bsonType: "int" }
                }
              }
            }
          }
        }
      }
    }
  }
});
db.inferences.createIndex({created_at: -1});
db.inferences.createIndex({"detections.class": 1});
db.inferences.createIndex({brand: 1});
