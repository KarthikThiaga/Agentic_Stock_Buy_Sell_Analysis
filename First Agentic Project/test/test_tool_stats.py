from storage.read_tool_stats import read_tool_stats
from storage.write_tool_stats import write_tool_stats
from storage.update_tool_stats import update_tool_stats

def test_read_tool_stats():
    # Test that the function returns a dictionary
    # stats = read_tool_stats()
    # assert isinstance(stats, dict), f"Expected a dictionary but got {type(stats)}"

    # Test that the function returns an empty dictionary if the file does not exist
    # (This will depend on the state of your file system, so you may want to mock this)
    # For now, we will just check that it does not raise an exception and returns a dictionary
    try:
        stats = read_tool_stats()
        assert isinstance(stats, dict), f"Expected a dictionary but got {type(stats)}"
    except Exception as e:
        assert False, f"Expected no exception but got {e}"

def test_update_tool_stats():
    # Test that the function updates the stats correctly
    # We will mock the read and write functions to test this in isolation
    # For now, we will just check that it does not raise an exception

    stats = read_tool_stats()
    stats_for_test_tool_before = stats.get("test_tool", {})
    
    try:
        update_tool_stats("test_tool","primary" ,True)
    except Exception as e:
        assert False, f"Expected no exception but got {e}"  

    stats = read_tool_stats()
    stats_for_test_tool_after = stats.get("test_tool", {})
    assert stats_for_test_tool_after.get("successes", 0) == stats_for_test_tool_before.get("successes", 0) + 1

    stats = read_tool_stats()
    stats_for_test_tool_before = stats.get("test_tool", {})

    try:
        update_tool_stats("test_tool","primary" ,False)
    except Exception as e:
        assert False, f"Expected no exception but got {e}"

    stats = read_tool_stats()
    stats_for_test_tool_after = stats.get("test_tool", {})

    assert stats_for_test_tool_after.get("failures", 0) == stats_for_test_tool_before.get("failures", 0) + 1

    stats = read_tool_stats()
    stats_for_test_tool_before = stats.get("test_tool", {})

    try:
        update_tool_stats("test_tool","fallback" ,True)
    except Exception as e:
        assert False, f"Expected no exception but got {e}"

    stats = read_tool_stats()
    stats_for_test_tool_after = stats.get("test_tool", {})
    assert stats_for_test_tool_after.get("fallback successes", 0) == stats_for_test_tool_before.get("fallback successes", 0) + 1

    stats = read_tool_stats()  
    stats_for_test_tool_before = stats.get("test_tool", {})

    try:
        update_tool_stats("test_tool","fallback" ,False)    
    except Exception as e:
        assert False, f"Expected no exception but got {e}"  
    
    stats = read_tool_stats()
    stats_for_test_tool_after = stats.get("test_tool", {})

    assert stats_for_test_tool_after.get("fallback failures", 0) == stats_for_test_tool_before.get("fallback failures", 0) + 1

    stats = read_tool_stats()
    stats_for_test_tool_after = stats.get("test_tool", {})

    stats = read_tool_stats()
    stats_for_test_tool_before = stats.get("test_tool", {})

    update_tool_stats("test_tool","abc" ,True)

    stats = read_tool_stats()
    stats_for_test_tool_after = stats.get("test_tool", {})

    assert stats_for_test_tool_after == stats_for_test_tool_before
    
    
    