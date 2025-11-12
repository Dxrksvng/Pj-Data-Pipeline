# file: create_supply_chain_checkpoint.py
import great_expectations as gx

# 1. สร้าง Data Context
context = gx.get_context()

# 2. ดึง Datasource และ Asset ที่มีอยู่แล้ว
datasource = context.datasources["pg_datasource"]
asset = datasource.get_asset("stg_supply_chain_asset")

# 3. สร้างหรืออัปเดต Checkpoint
checkpoint_name = "stg_supply_chain_checkpoint"
checkpoint = context.add_or_update_checkpoint(
    name=checkpoint_name,
    validations=[
        {
            "batch_request": asset.build_batch_request(),
            "expectation_suite_name": "stg_supply_chain_suite",
        }
    ]
)

print(f"✅ Checkpoint '{checkpoint_name}' is created.")
# # รันทดสอบทันที
# result = context.run_checkpoint(checkpoint_name)
# print(f"Checkpoint run result: {result['success']}")

# for vr in result['run_results'].values():
#     validation_result = vr['validation_result']
#     for exp in validation_result['results']:
#         print(exp['expectation_config']['expectation_type'], exp['success'])