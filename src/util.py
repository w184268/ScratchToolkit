def is_spcial(idinfo: dict):
    return idinfo['opcode'].startswith('operator_') or idinfo['opcode'] in ()