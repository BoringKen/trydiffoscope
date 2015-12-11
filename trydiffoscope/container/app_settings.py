DOCKER_IMAGE = 'trydiffoscope'
DOCKER_MEMORY_LIMIT = '500m'
DOCKER_DROP_CAPABILITIES = (
    'audit_control',
    'audit_write',
    'mac_admin',
    'mac_override',
    'mknod',
    'setfcap',
    'setpcap',
    'sys_admin',
    'sys_boot',
    'sys_module',
    'sys_nice',
    'sys_pacct',
    'sys_rawio',
    'sys_resource',
    'sys_time',
    'sys_tty_config',
)
