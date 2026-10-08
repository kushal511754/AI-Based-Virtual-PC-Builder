from server.services.pc_build_agent import PCBuildAgent

result = PCBuildAgent.generate_build('video_editing', 75000, 'Adobe Premiere')
print('Success:', result['success'])
print('Message:', result.get('message'))
if result['success']:
    for part, data in result.get('parts', {}).items():
        if data:
            print(f'{part}: {data.get("name")} - Rs. {data.get("price_inr")}')
        else:
            print(f'{part}: None')
else:
    print('Validation logs:', result.get('validation_logs'))
