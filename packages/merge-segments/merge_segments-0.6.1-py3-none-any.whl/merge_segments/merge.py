from enum import Enum
from typing import Optional, List, Tuple
from deprecated import deprecated

import numpy as np
import pandas
import pandas as pd


class AggregationType(Enum):
	KeepLongestSegment       = 1 # Deprecated
	KeepLongest              = 2
	Average                  = 3
	LengthWeightedAverage    = 4
	LengthWeightedPercentile = 5
	First                    = 6
	SumProportionOfData      = 7
	SumProportionOfTarget    = 8
	Sum                      = 9
	IndexOfMax               = 10
	IndexOfMin               = 11
	Min                      = 12
	Max                      = 13


class Aggregation:
	
	def __init__(self, aggregation_type: AggregationType, percentile: Optional[float] = None):
		"""Don't initialise this class directly, please use one of the static factory functions"""
		self.type: AggregationType = aggregation_type
		self.percentile: Optional[float] = percentile
		pass
	
	@staticmethod
	def First():
		return Aggregation(AggregationType.First)
	
	@staticmethod
	@deprecated(version="0.1.0", reason="`merge.Aggregation.KeepLongestSegment()` is an old, incorrect implementation. Please use `merge.Aggregation.KeepLongest()`")
	def KeepLongestSegment():
		"""
		DEPRECATED: Please use `KeepLongest()` instead.
		"""
		#print("WARNING `KeepLongestSegment` is deprecated, please use `KeepLongest` instead.\n`KeepLongestSegment` kept here temporarily for testing purposes but is will be removed in future versions.")
		return Aggregation(AggregationType.KeepLongestSegment)
	
	@staticmethod
	def KeepLongest():
		return Aggregation(AggregationType.KeepLongest)
	
	@staticmethod
	def LengthWeightedAverage():
		return Aggregation(AggregationType.LengthWeightedAverage)
	
	@staticmethod
	def Average():
		"""
		The average non-blank overlapping value. If all overlapping values are blank, keep blank.
		"""
		return Aggregation(AggregationType.Average)
	
	@staticmethod
	def LengthWeightedPercentile(percentile: float):
		"""
		The length weighted percentile of overlapping values.
		This is similar to a normal percentile calculation, but the length of the overlapping segment is taken into account.

		There is a complicated sort-by-Value, followed by an interpolation step.
		In the following diagram the `▴` shows the value of the 75th percentile.
		The `▴` is at 75% of the total length (chainage/SLK length) of all overlapping values
		(not including the length of half the first segment and half the last segment)
		and is interpolated between center-point values (`○`) of the last two segments:
		
		```text
		      |                          _○_
		      |                         |   |
		      |                      ▴  |   |   <---- 75th percentile value
		Value |              _____○_____|   |
		      |        __○__|           |   |
		      |       |     |           |   |
		      |  __○__|     |           |   |
		      | |     |     |           |   |
		           |<-----SLK Length----->|
		           0%                ↑   100%
		                             │
		      75th percentile ───────┘
		```
		"""
		if percentile > 1.0 or percentile < 0.0:
			raise ValueError(
				f"Percentile out of range. Must be greater than 0.0 and less than 1.0. Got {percentile}." +
				(" Do you need to divide by 100?" if percentile > 1.0 else "")
			)
		return Aggregation(
			AggregationType.LengthWeightedPercentile,
			percentile=percentile
		)
	
	@staticmethod
	@deprecated(version="0.4.3", reason="Aggregation type is renamed; Please use `Aggregation.SumProportionOfData()` for equivalent behaviour.")
	def ProportionalSum():
		"""
		DEPRECATED: Please use `merge.Aggregation.SumProportionOfData()` for equivalent behaviour. `ProportionalSum()` will be removed in the future.
		
		The sum of all overlapping `data` segments,
		where the value of each overlapping segment is multiplied by
		the length of the overlap divided by the length of the `data` segment.
		This is the same behaviour as the old VBA macro.
		See also `SumProportionOfTarget()`
		"""
		return Aggregation(AggregationType.SumProportionOfData)

	@staticmethod
	def SumProportionOfTarget():
		"""
		The sum of all overlapping `data` segments,
		where the value of each overlapping segment is multiplied by
		the length of the overlap divided by the length of the `target` segment.
		
		This aggregation method is suitable when aggregating columns measured in
		`Units per Kilometre` or `% of length`. The aggregated value will have the same unit.
		The assumption is that the % of length is spread evenly across the whole data segment.
		(This aggregation was created to deal with the cracking dataset which is given in 10 metre segments with a % cracked.
		Note that a better aggregation should be used if there is concern regarding the relative width between the `data` and `target` segments)

		The result below is calculated as `result = (20%*10 + 40%*5)/40 = 10%`

		```text
		data   :   |-- len=20---value=20% --|                 |----------------------- len=50 --- value=40% ----------------|
		target :              |------------- len=40 ------------------|
		overlap:              |--- len=10 --|                 |-len=5-|
		result :              |------------ value=10% ----------------|
		```
		
		See also `SumProportionOfData()`
		"""
		return Aggregation(AggregationType.SumProportionOfTarget)

	@staticmethod
	def SumProportionOfData():
		"""
		The sum of all overlapping `data` segments,
		where the value of each overlapping segment is multiplied by
		the length of the overlap divided by the length of the `data` segment.
		This is the same behaviour as the old VBA macro.
		See also `SumProportionOfTarget()`
		"""
		return Aggregation(AggregationType.SumProportionOfData)

	@staticmethod
	def Sum():
		"""This is the sum of values touching the target. Even if only part of the value is overlapping the target segment, the entire data value will be added to the sum"""
		return Aggregation(AggregationType.Sum)

	@staticmethod
	def IndexOfMax():
		"""The index (or row label) of the `data` DataFrame, of the maximum overlapping segment"""
		return Aggregation(AggregationType.IndexOfMax)
	
	@staticmethod
	def IndexOfMin():
		"""The index (or row label) of the `data` DataFrame, of the minimum overlapping segment"""
		return Aggregation(AggregationType.IndexOfMin)

	@staticmethod
	def Max():
		"""Value of the maximum overlapping segment"""
		return Aggregation(AggregationType.Max)
	
	@staticmethod
	def Min():
		"""Value of the minimum overlapping segment"""
		return Aggregation(AggregationType.Min)


class Action:
	def __init__(
			self,
			column_name: str,
			aggregation: Aggregation,
			rename: Optional[str] = None
	):
		self.column_name: str = column_name
		self.rename = rename if rename is not None else self.column_name
		self.aggregation: Aggregation = aggregation


def on_slk_intervals(target: pd.DataFrame, data: pd.DataFrame, join_left: List[str], column_actions: List[Action], from_to: Tuple[str, str]):
	slk_from, slk_to = from_to
	
	result_index = []
	result_rows = []

	if not isinstance(join_left, list):
		raise Exception("Parameter `join_left` must be a list literal. Tuples and other sequence types will lead to cryptic errors from pandas.")
	
	# prevent confusing error if user accidentally passes in a series instead of a dataframe
	if not isinstance(data, pd.DataFrame):
		raise TypeError(f"`data` parameter must be a pandas dataframe, received data of type {type(data)}")
		
	if not isinstance(target, pd.DataFrame):
		raise TypeError(f"`target` parameter must be a pandas dataframe, received target of type {type(target)}")

	# prevent an error that occurs when the secondary dataframe has a multi index;
	# TODO: why does it even happen in the first place?
	if isinstance(target.index, pd.MultiIndex):
		raise Exception("the `target` dataframe uses a `pandas.MultiIndex` which is not currently supported. please use `target.reset_index()` to revert to a normal index.")
	if isinstance(data.index, pd.MultiIndex):
		raise Exception("the `data` dataframe uses a `pandas.MultiIndex` which is not currently supported. please use `data.reset_index()` to revert to a normal index.")
	if isinstance(target.columns, pd.MultiIndex):
		raise Exception("the `target` dataframe uses a `pandas.MultiIndex` for a column index which is not currently supported.")
	if isinstance(data.columns, pd.MultiIndex):
		raise Exception("the `data` dataframe uses a `pandas.MultiIndex` for a column index which is not currently supported.")
	if target.index.has_duplicates:
		raise Exception("`target` dataframe has a duplicated index. please use `target.reset_index()` to fix.")
	if data.index.has_duplicates:
		#this check is maybe not required since this algorithim will re-index data anyway?
		raise Exception("`data` dataframe has a duplicated index. please use `data.reset_index()` to fix.")
	if target.columns.has_duplicates:
		raise Exception("`target` dataframe has a duplicated column names.")
	if data.columns.has_duplicates:
		raise Exception("`data` dataframe has a duplicated column names.")
	
	

	# prevent doing a lot of work then getting an error from pandas 
	# join about not specifying a suffix for overlapping column names
	for column_action in column_actions:
		if column_action.rename in target.columns:
			if column_action.column_name == column_action.rename:
				raise Exception(f"Cannot merge column '{column_action.column_name}' into target because the target already contains a column of that name. Please consider using the rename parameter; `Action(..., rename='xyz')`")
			else:
				raise Exception(f"Cannot merge column '{column_action.column_name}' as '{column_action.rename}' into target because the target already contains a column named '{column_action.rename}'.")

	missing_columns = []
	for column_name in join_left+list(from_to):
		if column_name not in data.columns and column_name not in target.columns:
			missing_columns.append(f"Column '{column_name}' is missing from both `target` and `data`.")
		elif column_name not in data.columns:
			missing_columns.append(f"Column '{column_name}' is missing from `data`.")
		elif column_name not in target.columns:
			missing_columns.append(f"Column '{column_name}' is missing from `target`.")
	if len(missing_columns) > 0:
		raise Exception(
			"Please check the `join_left` and `from_to` parameters."
			"Specified columns must be present and have matching names in both `target` and `data`:\n"
			"\n".join(missing_columns)
		)

	# prevent execution if there are zero-length rows
	if (data[slk_from]==data[slk_to]).any():
		raise Exception("`data` dataframe has rows where from=to. The merge tool does not work with zero length segments. Please adjust to give the segments some length.")
	if (target[slk_from]==target[slk_to]).any():
		raise Exception("`target` dataframe has rows where from=to. The merge tool does not work with zero length segments. Please adjust to give the segments some length.")

	# ReIndex data for faster O(N) lookup
	data = data.assign(data_id=data.index)
	data = data.set_index([*join_left, 'data_id'])
	data = data.sort_index()
	
	# Group target data by Road Number and Carriageway
	try:
		target_groups = target.groupby(join_left)
	except KeyError:
		matching_columns = [col for col in join_left if col in target.columns]
		raise Exception(f"Parameter join_left={join_left} did not match" + (
			" any columns in the target DataFrame" if len(matching_columns) == 0
			else f" all columns in target DataFrame. Only matched columns {matching_columns}"
		))
	

	
	# Main Loop
	# TODO: address pandas warning regarding groupers with length of 1; will not return a tuple. Annoying, why?
	for target_group_index, target_group in target_groups:
		try:
			data_matching_target_group = data.loc[target_group_index]
		except KeyError:
			# There was no data matching the target group. Skip adding output. output to these rows will be NaN for all columns.
			continue
		except TypeError as e:
			# The datatype of group_index is picky... sometimes it wants a tuple, sometimes it will accept a list
			# this appears to be a bug or inconsistency with pandas when using multi-index dataframes.
			print(f"Error: Could not group the following data by {target_group_index}:")
			print(f"type(group_index)  {type(target_group_index)}:")
			print("the data:")
			print(data)
			raise e
		
		# Iterate row by row through the target group
		for target_index, target_row in target_group.iterrows():
			
			# Select data with overlapping slk interval
			data_to_aggregate_for_target_group = data_matching_target_group[
				(data_matching_target_group[slk_from] < target_row[slk_to]) &
				(data_matching_target_group[slk_to] > target_row[slk_from])
			]#.copy()
			# TODO: the copy function on the line above has a lot to do with the slowness of this algorithm
			#       because all columns are copied, not just the ones we are aggregating, for wide dataframes
			#       there is potentially a huge amount of memory allocated and deallocated that doesnt need to be.
			#       only needs to be copied so that the "overlap_len" column can be added. If we can avoid adding
			#       this column we might do a lot better.
			
			# if no data matches the target group then skip
			if data_to_aggregate_for_target_group.empty:
				continue
			
			# compute overlaps for each row of data
			overlap_min = np.maximum(data_to_aggregate_for_target_group[slk_from], target_row[slk_from])
			overlap_max = np.minimum(data_to_aggregate_for_target_group[slk_to],   target_row[slk_to])
			
			# overlap_len = np.maximum(overlap_max - overlap_min, 0)  # np.maximum() is not needed due to filters above
			overlap_len = overlap_max - overlap_min
			
			# expect this to trigger warning about setting value on view?
			# does not seem to though
			#data_to_aggregate_for_target_group["overlap_len"] = overlap_len  # Remove this... there is no reason to attached overlap_len to the original dataframe
			
			# for each column of data that we keep, we must aggregate each field down to a single value
			# create a blank row to store the result of each column
			aggregated_result_row = []
			for column_action_index, column_action in enumerate(column_actions):

				column_len_to_aggregate: pd.DataFrame = (
					data_to_aggregate_for_target_group
					.loc[:, [column_action.column_name]]
					.assign(overlap_len=overlap_len)  # assign is done here so that NaN data can be dropped at the same time as the overlap lengths. Later we also benefit from the combination by being able to concurrently sort both columns.
				)
				column_len_to_aggregate = column_len_to_aggregate[
					~ column_len_to_aggregate.iloc[:, 0].isna() &
					  (column_len_to_aggregate["overlap_len"] > 0)
				]
				
				if column_len_to_aggregate.empty:
					# Infill with np.nan or we will lose our column position.
					aggregated_result_row.append(np.nan)
					continue
				
				column_to_aggregate:             pandas.Series = column_len_to_aggregate.iloc[:, 0]
				column_to_aggregate_overlap_len: pandas.Series = column_len_to_aggregate.iloc[:, 1]
				
				if column_action.aggregation.type   == AggregationType.Average:
					aggregated_result_row.append(
						column_to_aggregate.mean()
					)
					
				elif column_action.aggregation.type == AggregationType.First:
					aggregated_result_row.append(column_to_aggregate.iloc[0])
				
				elif column_action.aggregation.type == AggregationType.LengthWeightedAverage:
					total_overlap_length = column_to_aggregate_overlap_len.sum()
					aggregated_result_row.append(
						(column_to_aggregate * column_to_aggregate_overlap_len).sum() / total_overlap_length
					)

				elif column_action.aggregation.type == AggregationType.KeepLongestSegment:
					aggregated_result_row.append(
						column_to_aggregate.loc[column_to_aggregate_overlap_len.idxmax()]
					)

				elif column_action.aggregation.type == AggregationType.KeepLongest:
					aggregated_result_row.append(
						column_to_aggregate_overlap_len.groupby(column_to_aggregate).sum().idxmax()
					)

				elif column_action.aggregation.type == AggregationType.LengthWeightedPercentile:
					column_len_to_aggregate = column_len_to_aggregate.sort_values(
						by=column_action.column_name,
						ascending=True
					)

					column_to_aggregate:             pandas.Series = column_len_to_aggregate.iloc[:, 0] # TODO: Why is this repeated?
					column_to_aggregate_overlap_len: pandas.Series = column_len_to_aggregate.iloc[:, 1] # TODO: Why is this repeated?
					
					x_coords = (column_to_aggregate_overlap_len.rolling(2).mean()).fillna(0).cumsum()
					x_coords /= x_coords.iloc[-1]
					result = np.interp(
						column_action.aggregation.percentile,
						x_coords.to_numpy(),
						column_to_aggregate
					)
					aggregated_result_row.append(result)

				elif column_action.aggregation.type == AggregationType.SumProportionOfData:
					data_to_aggregate_for_target_group_slk_length = data_to_aggregate_for_target_group[slk_to]-data_to_aggregate_for_target_group[slk_from]
					aggregated_result_row.append(
						(column_to_aggregate * column_to_aggregate_overlap_len/data_to_aggregate_for_target_group_slk_length).sum()
					)

				elif column_action.aggregation.type == AggregationType.SumProportionOfTarget:
					# data_to_aggregate_for_target_group_slk_length = data_to_aggregate_for_target_group[slk_to]-data_to_aggregate_for_target_group[slk_from]
					target_length = target_row[slk_to] - target_row[slk_from]
					aggregated_result_row.append(
						(column_to_aggregate * column_to_aggregate_overlap_len).sum()/target_length
					)
				
				elif column_action.aggregation.type == AggregationType.Sum:
					aggregated_result_row.append(
						column_to_aggregate.sum()
					)

				elif column_action.aggregation.type == AggregationType.IndexOfMax:
					aggregated_result_row.append(
						column_to_aggregate.idxmax()
					)

				elif column_action.aggregation.type == AggregationType.IndexOfMin:
					aggregated_result_row.append(
						column_to_aggregate.idxmin()
					)

				elif column_action.aggregation.type == AggregationType.Max:
					aggregated_result_row.append(
						column_to_aggregate.max()
					)

				elif column_action.aggregation.type == AggregationType.Min:
					aggregated_result_row.append(
						column_to_aggregate.min()
					)
				
				
			
			result_index.append(target_index)
			result_rows.append(aggregated_result_row)
	
	result = target.join(
		pd.DataFrame(
			result_rows,
			columns=[x.rename for x in column_actions],
			index=result_index
		)
	)
	if len(result.index) != len(target.index):
		raise Exception("Oh no... the merge algorithim has somehow created addtional rows :O. This is a rare bug that I think is fixed now, but if you do see this message please contact the author.")
	return result
