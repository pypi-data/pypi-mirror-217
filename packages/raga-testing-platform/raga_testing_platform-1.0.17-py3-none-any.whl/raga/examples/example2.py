from raga import *
import pandas as pd
import json

ds_json_file = "test-dataset-modelG.json"

test_df = []
with open(ds_json_file, 'r') as json_file:
    # Load JSON data
    json_data = json.load(json_file)
    
    # Process the JSON data
    transformed_data = []
    for item in json_data:
        AnnotationsV1 = ImageDetectionObject()
        ROIVectorsM1 = ROIEmbedding()
        ImageVectorsM1 = ImageEmbedding()
        for detection in item["outputs"][0]["detections"]:
            AnnotationsV1.add(ObjectDetection(Id=0, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            for roi_emb in detection['roi_embedding']:
                ROIVectorsM1.add(Embedding(roi_emb))
        
        attributes_dict = {}
        attributes = item.get("attributes", {})
        for key, value in attributes.items():
            attributes_dict[key] = StringElement(value)

        image_embeddings = item.get("image_embedding", {})
        for value in image_embeddings:
            ImageVectorsM1.add(Embedding(value))

        data_point = {
            'ImageId': StringElement(item["inputs"][0]),
            'TimeOfCapture': TimeStampElement(item["capture_time"]),
            'SourceLink': StringElement(item["inputs"][0]),
            'AnnotationsGroundTruth': AnnotationsV1,
            'ImageVectorsGroundTruth': ROIVectorsM1,
            'ROIVectorsGroundTruth': ImageVectorsM1,
        }

        merged_dict = {**data_point, **attributes_dict}

        test_df.append(merged_dict)
        

pd_data_frame = pd.DataFrame(test_df)


#create schema object of RagaSchema instance
# schema = RagaSchema()
# schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
# schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
# schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
# schema.add("Reflection", AttributeSchemaElement(), pd_data_frame)
# schema.add("Overlap", AttributeSchemaElement(), pd_data_frame)
# schema.add("CameraAngle", AttributeSchemaElement(), pd_data_frame)
# schema.add("AnnotationsGroundTruth", InferenceSchemaElement(model="Testing-groundTruth"), pd_data_frame)
# schema.add("ImageVectorsGroundTruth", ImageEmbeddingSchemaElement(model="Testing-groundTruth", ref_col_name=""), pd_data_frame)
# schema.add("ROIVectorsGroundTruth", RoiEmbeddingSchemaElement(model="Testing-groundTruth", ref_col_name=""), pd_data_frame)

project_name = "testingProject" # Project Name
run_name= "test-exp-jun-new-18" # Experiment Name
dataset_name = "test-dataset-jun-new-1" # Dataset Name


#create test_session object of TestSession instance
test_session = TestSession(project_name=project_name,run_name=run_name)

#create test_ds object of Dataset instance
# test_ds = Dataset(test_session=test_session, name=dataset_name)

#load schema and pandas data frame
# test_ds.load(pd_data_frame, schema)






# Params for unlabelled AB Model Testing

testName = StringElement("test-labelled-jun-1")
modelA = StringElement("Testing-modelA")
modelB = StringElement("Testing-modelB")
gt = StringElement("Testing-groundTruth")
type = ModelABTestTypeElement("labelled")
aggregation_level = AggregationLevelElement()
aggregation_level.add(StringElement("Reflection"))
aggregation_level.add(StringElement("Overlap"))
aggregation_level.add(StringElement("CameraAngle"))
rules = ModelABTestRules()
rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("ALL"), threshold = FloatElement(0.5))

#create payload for model ab testing
model_comparison_check = model_ab_test(test_session, dataset_name=dataset_name, testName=testName, modelA = modelA , modelB = modelB , type = type, aggregation_level = aggregation_level, rules = rules, gt=gt)


#add payload into test_session object
test_session.add(model_comparison_check)

#run added ab test model payload
test_session.run()