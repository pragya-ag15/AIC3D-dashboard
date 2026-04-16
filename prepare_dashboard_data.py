import pandas as pd

# LODO rows
lodo_rows = [
    ["Experiment 1: Diverse drugs", "LinearRegression", "Amoxicillin", 3.6854, 1.3372, -3.1135],
    ["Experiment 1: Diverse drugs", "LinearRegression", "Clarithromycin", 19.7479, 4.2314, -0.6313],
    ["Experiment 1: Diverse drugs", "LinearRegression", "Trimethoprim", 6.7362, 2.4933, -11.3208],
    ["Experiment 1: Diverse drugs", "RandomForest", "Amoxicillin", 1.3179, 0.8282, -0.4709],
    ["Experiment 1: Diverse drugs", "RandomForest", "Clarithromycin", 15.9342, 3.7594, -0.3162],
    ["Experiment 1: Diverse drugs", "RandomForest", "Trimethoprim", 1.1844, 0.9511, -1.1664],

    ["Experiment 2: NSAIDs (similar class)", "LinearRegression", "Aspirin", 0.4261, 0.6431, -37.2554],
    ["Experiment 2: NSAIDs (similar class)", "LinearRegression", "Diclofenac", 0.3236, 0.4946, -0.3102],
    ["Experiment 2: NSAIDs (similar class)", "LinearRegression", "Ibuprofen", 0.2148, 0.4069, -14.6489],
    ["Experiment 2: NSAIDs (similar class)", "LinearRegression", "Naproxen", 0.1226, 0.3262, -1.9776],
    ["Experiment 2: NSAIDs (similar class)", "LinearRegression", "Paracetamol", 1.6285, 1.0785, -2.5498],
    ["Experiment 2: NSAIDs (similar class)", "RandomForest", "Aspirin", 0.5717, 0.7521, -50.3268],
    ["Experiment 2: NSAIDs (similar class)", "RandomForest", "Diclofenac", 0.3397, 0.5384, -0.3752],
    ["Experiment 2: NSAIDs (similar class)", "RandomForest", "Ibuprofen", 0.1058, 0.2736, -6.7072],
    ["Experiment 2: NSAIDs (similar class)", "RandomForest", "Naproxen", 0.9583, 0.9013, -22.2688],
    ["Experiment 2: NSAIDs (similar class)", "RandomForest", "Paracetamol", 5.5348, 2.2292, -11.0646],
]
lodo_df = pd.DataFrame(lodo_rows, columns=["Experiment", "Model", "Drug", "MSE", "MAE", "R2"])
lodo_df.to_csv("AIC3D_v2_lodo_both.csv", index=False)

# Summary
summary_df = pd.DataFrame([
    ["Experiment 1: Diverse drugs", 0.7641, -21.2320, -0.0677, 9, "pH"],
    ["Experiment 2: NSAIDs (similar class)", 0.9158, 0.7157, 0.2327, 17, "Structure"]
], columns=["Experiment", "TrainTest_RF_R2", "CV_RF_R2", "LODO_RF_R2", "Points", "DominantSignal"])
summary_df.to_csv("AIC3D_v2_summary.csv", index=False)

# Feature importance
feature_df = pd.DataFrame([
    ["Experiment 1: Diverse drugs", "pH", 0.622647],
    ["Experiment 1: Diverse drugs", "LogP", 0.115581],
    ["Experiment 1: Diverse drugs", "MW", 0.103378],
    ["Experiment 1: Diverse drugs", "TPSA", 0.088683],
    ["Experiment 1: Diverse drugs", "HBA", 0.066999],
    ["Experiment 1: Diverse drugs", "HBD", 0.002712],
    ["Experiment 2: NSAIDs (similar class)", "MW", 0.458990],
    ["Experiment 2: NSAIDs (similar class)", "HBD", 0.285239],
    ["Experiment 2: NSAIDs (similar class)", "TPSA", 0.115907],
    ["Experiment 2: NSAIDs (similar class)", "pH", 0.067660],
    ["Experiment 2: NSAIDs (similar class)", "LogP", 0.067236],
    ["Experiment 2: NSAIDs (similar class)", "HBA", 0.004968],
], columns=["Experiment", "Feature", "Importance"])
feature_df.to_csv("AIC3D_v2_feature_importance.csv", index=False)

# Metrics
metrics_df = pd.DataFrame([
    ["Experiment 1: Diverse drugs", "LinearRegression", 2.7993, 0.4864, 15.3486, -48.1190, 10.0565, 2.6873, -0.7472],
    ["Experiment 1: Diverse drugs", "RandomForest", 1.2857, 0.7641, 7.0386, -21.2320, 6.1455, 1.8463, -0.0677],
    ["Experiment 2: NSAIDs (similar class)", "LinearRegression", 0.1886, 0.8861, 0.5369, 0.7479, 0.5762, 0.5944, 0.7389],
    ["Experiment 2: NSAIDs (similar class)", "RandomForest", 0.1394, 0.9158, 0.6231, 0.7157, 1.6936, 1.0000, 0.2327],
], columns=[
    "Experiment", "Model", "TrainTest_MSE", "TrainTest_R2",
    "CV_MSE", "CV_R2", "LODO_MSE_Overall", "LODO_MAE_Overall", "LODO_R2_Overall"
])
metrics_df.to_csv("AIC3D_v2_metrics.csv", index=False)

print("Saved dashboard data files.")
