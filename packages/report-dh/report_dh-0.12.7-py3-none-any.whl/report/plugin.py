import pytest
from ._data import parse
from ._internal import Launch
import traceback


parse()


def add_fixtures_to_teardown(fixture_name, teardown_name):
        item_id = Launch.create_report_item(
                name=fixture_name,
                parent_item=teardown_name,
                type='step',
                description='',
                has_stats=False)

        Launch.add_item(fixture_name, item_id)


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "my_custom_marker: My custom marker with additional functionality")

def pytest_addoption(parser):
    parser.addoption("--report", action="store_true")


def pytest_sessionstart(session):
    script_path = session.config.getoption("--report")
    if script_path:
        parse()
        Launch.start_launch()


def pytest_sessionfinish(session, exitstatus):
    script_path = session.config.getoption("--report")
    if script_path:
        for item in Launch.items().keys():
            Launch.finish_item(item)
        Launch.finish_launch()


@pytest.hookimpl(tryfirst=True)
def pytest_fixture_setup(fixturedef, request):
    fixture_name = request.fixturename
    if fixture_name and '_xunit_setup_class' not in fixture_name:
        if request.scope in ['class', 'function']:
            required_fixture = getattr(request.cls, request.fixturename, None)
            new_fixture_name = getattr(required_fixture, '__new_name__', request.fixturename)

        else:
            function_fixture = request._fixturedef.func
            new_fixture_name = getattr(function_fixture, '__new_name__', request.fixturename)

        fixture_values = {}
        for fixture in request.fixturenames:
            if '{{{}}}'.format(fixture) in new_fixture_name:
                fixture_values[fixture] = request.getfixturevalue(fixture)

        parent = f'{request._pyfuncitem.name}_Setup'
        formatted_name = new_fixture_name.format(**fixture_values)
        item_id = Launch.create_report_item(
                name=formatted_name,
                parent_item=parent,
                type='step',
                has_stats=False,
                description='')
    
        Launch.add_item(request.fixturename, item_id)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    test_name = getattr(item.function, '__new_name__', item.name)
    test_name = getattr(item.function, '__new_name__')
    if item.name not in Launch.items() and item.parent is not None:
        attributes = [marker.name for marker in item.iter_markers()]
        item_id = Launch.create_report_item(
            name=test_name,
            parent_item=item.parent.name,
            type='scenario',
            has_stats=True,
            description='',
            attributes=attributes)

        Launch.add_item(item.name, item_id)
        attributes = [marker.name for marker in item.iter_markers()]
        item_is_not_skipped = 'skip' not in attributes
        
        if 'skip' in attributes:
            marker = item.get_closest_marker("skip")
            skip_reason = marker.kwargs.get("reason")
            Launch.finish_skipped_item(item.name, skip_reason)
        
        if item_is_not_skipped:
            item_setup_name = f'Setup'
            item_id = Launch.create_report_item(
                name=item_setup_name,
                parent_item=item.name,
                type='before_test',
                has_stats=True,
                description='')

            Launch.add_item(f'{item.name}_{item_setup_name}', item_id)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    item_teardown_name = 'Teardown'
    attributes = [marker.name for marker in item.iter_markers()]
    item_is_not_skipped = 'skip' not in attributes
    if item_is_not_skipped:
        item_id = Launch.create_report_item(
            name=item_teardown_name,
            parent_item=item.name,
            type='after_test',
            has_stats=True,
            description='')

        teardown_name = f'{item.name}_{item_teardown_name}'
        Launch.add_item(teardown_name, item_id)

        for fixture in item.fixturenames:
            if '_xunit_setup_class' not in fixture:
                add_fixtures_to_teardown(fixture, teardown_name)
                item._fixtureinfo.name2fixturedefs[fixture][0].addfinalizer(lambda: Launch.finish_item(fixture))


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    excinfo = call.excinfo
    attributes = [marker.name for marker in item.iter_markers()]
    item_is_not_skipped = 'skip' not in attributes
    if item_is_not_skipped:
        if call.when == 'setup':
            run_item_teardown(f'{item.name}_Setup', excinfo)

        if call.when == 'call':
            run_item_teardown(f'{item.name}_Execution', excinfo)

        if call.when == 'teardown':
            run_item_teardown(f'{item.name}_Teardown', excinfo)
        


def run_item_teardown(item_name: str, excinfo):
    if excinfo is None:
        Launch.finish_passed_item(item_name)
        if 'Setup' in item_name:
            required_item = item_name.split('_Setup')
            add_item_execution(required_item[0])

    elif excinfo is not None:
        traceback_str = ''.join(traceback.format_tb(excinfo.tb))
        Launch.finish_failed_item(item_name, message=excinfo.typename, reason=traceback_str)


def add_item_execution(item_name):
    item_execution_name = 'Execution'
    item_id = Launch.create_report_item(
        name=item_execution_name,
        parent_item=item_name,
        type='step',
        has_stats=True,
        description='')

    Launch.add_item(f'{item_name}_{item_execution_name}', item_id)