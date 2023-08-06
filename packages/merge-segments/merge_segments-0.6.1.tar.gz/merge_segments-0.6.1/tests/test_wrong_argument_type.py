import pytest

def test_wrong_argument_type():
	import pandas as pd
	from merge_segments import merge

	segments = pd.DataFrame(
		columns=["road", "cwy", "slk_from", "slk_to"],
		data=[
			["H001", "L", 0, 100],
		]
	)

	data = pd.DataFrame(
		columns=["road", "cwy", "slk_from", "slk_to", "measure", "category"],
		data=[
			["H001", "L", 50, 140, 1.0, "A"],  # 50  40   0  0
			["H001", "L", 140, 160, 2.0, "B"],  # 0  20   0  0
		]
	)

	# null test omitted, some other test will fail.

	# This should raise an exception since target is a series
	with pytest.raises(TypeError, match="`target` parameter must be a pandas dataframe"):
		merge.on_slk_intervals(
			target        = segments["road"]=="H001",
			data          = data,
			join_left     = ["road", "cwy"],
			from_to       = ("slk_from", "slk_to"),
			column_actions= [
				merge.Action('measure',  rename="measure longest segment",  aggregation=merge.Aggregation.KeepLongest()),
			],
		)
	
	# This should raise an exception since data is a series
	with pytest.raises(TypeError, match="`data` parameter must be a pandas dataframe"):
		merge.on_slk_intervals(
			target        = segments,
			data          = data["road"]=="H001",
			join_left     = ["road", "cwy"],
			from_to       = ("slk_from", "slk_to"),
			column_actions= [
				merge.Action('measure',  rename="measure longest segment",  aggregation=merge.Aggregation.KeepLongest()),
			],
		)