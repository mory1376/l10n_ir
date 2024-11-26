# -*- coding: utf-8 -*-
{
    'name': 'Iran Localization (l10n_ir)',
    'summary': 'Localization for Iranian accounting standards and tax compliance.',
    'description': '''
    This module provides localization support for Iranian accounting standards, 
    including tax configurations, chart of accounts, and fiscal positions.
    ''',
    'author': 'Your Company Name',
    'website': 'https://erp.nettech.ir',
    'category': 'Localization',
    'version': '18.0.1.0',  # Updated versioning scheme for clarity
    'countries': ['ir'],
    # Dependencies: essential modules required for this module to work
    'depends': [
        'base',  # Core Odoo module
        'account',  # Core accounting functionality
        'account_accountant',  # Advanced accounting features
        'base_import',  # Import support
        'web',
        'base_address_extended'  # Web views and actions
    ],
    'auto_install': ['account'],
    # External Python dependencies (ensure these libraries are installed)
    'external_dependencies': {
        'python': ['persiantools', 'jdatetime'],  # Persian-specific tools
    },

    # Data files always loaded
    'data': [
        'views/account_move_views.xml',  # Custom account move views
        'views/res_config_settings_views.xml',  # Settings views
        'views/res_config.xml',  # Settings views
        'data/res.country.state.csv',
        'data/res.city.csv',

        'wizard/setup_wizard.xml',
        # QWeb templates (if needed)
    ],

    # Data files loaded only in demonstration mode

    'application': True,  # Marks this as a standalone application
    'installable': True,  # Indicates that this module is installable
}
