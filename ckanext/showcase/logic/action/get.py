import ckan.plugins.toolkit as toolkit
import ckan.lib.dictization.model_dictize as model_dictize
from ckan.lib.navl.dictization_functions import validate

from ckanext.showcase.logic.schema import (showcase_package_list_schema,
                                           package_showcase_list_schema)
from ckanext.showcase.model import ShowcasePackageAssociation, ShowcaseAdmin

import logging
log = logging.getLogger(__name__)


@toolkit.side_effect_free
def showcase_show(context, data_dict):
    '''Return the pkg_dict for a showcase (package).

    :param id: the id or name of the showcase
    :type id: string
    '''

    toolkit.check_access('ckanext_showcase_show', context, data_dict)

    pkg_dict = toolkit.get_action('package_show')(context, data_dict)

    return pkg_dict


@toolkit.side_effect_free
def showcase_list(context, data_dict):
    '''Return a list of all showcases in the site.'''

    toolkit.check_access('ckanext_showcase_list', context, data_dict)

    model = context["model"]

    q = model.Session.query(model.Package) \
        .filter(model.Package.type == 'showcase') \
        .filter(model.Package.state == 'active')

    showcase_list = []
    for pkg in q.all():
        showcase_list.append(model_dictize.package_dictize(pkg, context))

    return showcase_list


@toolkit.side_effect_free
def showcase_package_list(context, data_dict):
    '''List packages associated with a showcase.

    :param showcase_id: id or name of the showcase
    :type showcase_id: string

    :rtype: list of dictionaries
    '''

    toolkit.check_access('ckanext_showcase_package_list', context, data_dict)

    # validate the incoming data_dict
    validated_data_dict, errors = validate(data_dict,
                                           showcase_package_list_schema(),
                                           context)

    if errors:
        raise toolkit.ValidationError(errors)

    # get a list of package ids associated with showcase id
    pkg_id_list = ShowcasePackageAssociation.get_package_ids_for_showcase(
        validated_data_dict['showcase_id'])

    pkg_list = []
    if pkg_id_list:
        # for each package id, get the package dict and append to list if
        # active
        id_list = []
        for pkg_id in pkg_id_list:
<<<<<<< HEAD
<<<<<<< HEAD
            try:
<<<<<<< HEAD
<<<<<<< HEAD
                pkg = toolkit.get_action('package_show')(context,
                                                         {'id': pkg_id})
                if pkg['state'] == 'active':
                    pkg_list.append(pkg)
            except NotAuthorized:
                log.debug(
                    'Not authorized to access Package with ID: ' + str(pkg_id))
=======
                pkg = toolkit.get_action('package_show')(context, {'id': pkg_id})
                if pkg['state'] == 'active':
                    pkg_list.append(pkg)
            except NotAuthorized:
                log.error('Not authorized to access Package with ID: ' + str(pkg_id))

>>>>>>> fc7ff38 (except NotAuthorized when package can not be viewed)
=======
                pkg = toolkit.get_action('package_show')(context,
                                                         {'id': pkg_id})
                if pkg['state'] == 'active':
                    pkg_list.append(pkg)
            except NotAuthorized:
                log.error(
                    'Not authorized to access Package with ID: ' + str(pkg_id))
>>>>>>> 28d29a6 (except NotAuthorized when package can not be viewed)
=======
            id_list.append(pkg_id[0])

        q = ' OR '.join(id_list)
        pkg_list = toolkit.get_action('package_search')(
            context,
            {'q': q, 'rows': 100})
        pkg_list = pkg_list['results']

>>>>>>> ee7d155 (Batch list actions to a single query)
=======
            id_list.append(pkg_id[0])
        q = 'id:(' + ' OR '.join(['{0}'.format(x) for x in id_list]) + ')'
        _pkg_list = toolkit.get_action('package_search')(
            context,
            {'q': q, 'rows': 100})
        pkg_list = _pkg_list['results']
>>>>>>> 3cb90b1 (Use package_search to get related showcase/package)
    return pkg_list


@toolkit.side_effect_free
def package_showcase_list(context, data_dict):
    '''List showcases associated with a package.

    :param package_id: id or name of the package
    :type package_id: string

    :rtype: list of dictionaries
    '''

    toolkit.check_access('ckanext_package_showcase_list', context, data_dict)

    # validate the incoming data_dict
    validated_data_dict, errors = validate(data_dict,
                                           package_showcase_list_schema(),
                                           context)

    if errors:
        raise toolkit.ValidationError(errors)

    # get a list of showcase ids associated with the package id
    showcase_id_list = ShowcasePackageAssociation.get_showcase_ids_for_package(
        validated_data_dict['package_id'])
    showcase_list = []
<<<<<<< HEAD
    if showcase_id_list is not None:
        # for each package id, get the package dict and append to list if
        # active
        id_list = []
        for showcase_id in showcase_id_list:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 1f18935 (Merge pull request #2 from opendatazurich/fix-display-showcases)
            try:
                showcase = toolkit.get_action('package_show')(
                    context,
                    {'id': showcase_id}
                )
                showcase_list.append(showcase)
            except NotAuthorized:
                log.debug('Not authorized to access Package with ID: '
                          + str(showcase_id))
<<<<<<< HEAD

=======
            showcase = toolkit.get_action('package_show')(context,
                                                          {'id': showcase_id})
            showcase_list.append(showcase)
>>>>>>> 2cc3e65 (run test against multiple CKAN versions)
=======
>>>>>>> 1f18935 (Merge pull request #2 from opendatazurich/fix-display-showcases)
=======
            id_list.append(pkg_id[0])
=======
            id_list.append(showcase_id[0])
>>>>>>> 62ff22b (Fix syntax errors)

        q = ' OR '.join(id_list)
        showcase_list = toolkit.get_action('package_search')(
            context,
            {'q': q, 'rows': 100})
        showcase_list = showcase_list['results']

>>>>>>> ee7d155 (Batch list actions to a single query)
=======
    # import ipdb; ipdb.sset_trace()
    q = ''
    fq = ''
    if showcase_id_list:
        id_list = []
        for showcase_id in showcase_id_list:
            id_list.append(showcase_id[0])
        fq = 'dataset_type:showcase'
        q = 'id:(' + ' OR '.join(['{0}'.format(x) for x in id_list]) + ')'
        _showcase_list = toolkit.get_action('package_search')(
            context,
            {'q': q, 'fq': fq, 'rows': 100})
        showcase_list = _showcase_list['results']

>>>>>>> 3cb90b1 (Use package_search to get related showcase/package)
    return showcase_list


@toolkit.side_effect_free
def showcase_admin_list(context, data_dict):
    '''
    Return a list of dicts containing the id and name of all active showcase
    admin users.

    :rtype: list of dictionaries
    '''

    toolkit.check_access('ckanext_showcase_admin_list', context, data_dict)

    model = context["model"]

    user_ids = ShowcaseAdmin.get_showcase_admin_ids()

    if user_ids:
        q = model.Session.query(model.User) \
            .filter(model.User.state == 'active') \
            .filter(model.User.id.in_(user_ids))

        showcase_admin_list = []
        for user in q.all():
            showcase_admin_list.append({'name': user.name, 'id': user.id})
        return showcase_admin_list

    return []
