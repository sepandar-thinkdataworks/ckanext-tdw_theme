import ckan.plugins as p
import ckan.plugins.toolkit as t
from ckan.lib.base import BaseController
import routes.mapper

def get_groups_tdw():
    return t.get_action('group_list')(data_dict={'all_fields': True})

class TDWThemePlugin(p.SingletonPlugin):
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        t.add_template_directory(config, 'templates')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        t.add_public_directory(config, 'public')

        config['ckan.resource_proxy_enabled'] = True

    
    def get_helpers(self):
        return {'tdw_theme_get_groups': get_groups_tdw}

    def before_map(self,m):
#        with routes.mapper.SubMapper(route_map,
 #             controller='ckanext.tdw_theme.plugin:SuggestController') as m:
#           m.connect('suggest' ,'/suggest', action='suggest_form')
        m.connect('suggest' ,'/suggest',
                    controller='ckanext.tdw_theme.controller:SuggestController',
                    action='suggest_form')
        return m

    def after_map(self, route_map):
        return route_map
    
#class TDWThemeExtraPagesPlugin(p.SingletonPlugin):
 #   p.implements(p.IRoutes, inherit=True)
  #  p.implements(p.IConfigurer, inherit=True)

#    def before_map(self,route_map):
 #       with routes.mapper.SubMapper(route_map,
  #            controller='ckanext.tdw_theme.plugin:SuggestController') as m:
   #        m.connect('suggest' ,'/suggest', action='suggest_form')
    #    return m

#    def after_map(self, route_map):
 #       return route_map

