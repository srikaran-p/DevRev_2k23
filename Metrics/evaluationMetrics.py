import json

"""
metrics = Metrics()
metrics.exactMatch(a, b)
metrics.hallucination_rate(given_json, predicted_json)
metrics.f1_score_overall(predictedJson, requiredJson)
"""

class Metrics:
    def __init__(self):
        pass

    def __str__(self):
        pass

    def ordered(self, obj):
        """
        Helper Function

        Parameters:
        - obj = object

        Returns:
        - Sorted object if obj is of type dict or list
        - Else, we simply return the object
        """
        if isinstance(obj, dict):
            return sorted((k, self.ordered(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(self.ordered(x) for x in obj)
        else:
            return obj

    def get_tool_names(self, givenJson):
        """
        Helper Function

        Parameters:
        - givenJson = Json of the form, list of dictionaries

        Returns:
        - List of names of the tools used
        """
        tool_names = []
        for tool in givenJson:
            tool_names.append(tool["tool_name"])

        return tool_names

    def get_tool_descriptions(self, givenJson):
        """
        Helper Function

        Parameters:
        - givenJson = Json of the form, list of dictionaries

        Returns:
        - List of tool descriptions used in the json
        """
        tool_descriptions = []
        for tool in givenJson:
            tool_descriptions.append(tool)

        return tool_descriptions

    def get_arguments_names(self, givenTool):
        """
        Helper Function

        Parameters:
        - givenTool = Json of given tool

        Returns:
        - Argument names
        """
        arguments_names = []
        for arg in givenTool["arguments"]:
            arguments_names.append(arg["argument_name"])
        return arguments_names

    def get_arguments(self, givenTool):
        """
        Helper Function

        Parameters:
        - givenTool = Json of given tool

        Returns:
        - Argument details (name and value)
        """
        arguments_list = []
        for arg in givenTool["arguments"]:
            arguments_list.append(arg)

        return arguments_list

    def correct_elements(self, list1, list2):
        """
        Helper Function

        Parameters:
        - list1 = First list
        - list2 = Second list

        Returns:
        - List of common elements
        """
        return [element for element in list1 if element in list2]

    def average(self, list1):
        """
        Helper Function

        Parameters:
        - list1 = List of values

        Returns:
        - Average of the values
        """
        if len(list1) == 0:
            return 1
        else:
            return sum(list1)/len(list1)

    def precision(self, predictedList, requiredList):
        """
        Helper Function

        Parameters:
        - predictedList = List of predicted tools/arguments/values
        - requiredList = List of required tools/arguments/values

        Returns:
        - Precision of the prediction
        """
        if isinstance(predictedList, list) == False and isinstance(requiredList, list) == False:
            if predictedList == requiredList:
                return 1
            else:
                return 0

        correctValues = len(self.correct_elements(predictedList, requiredList))
        predictedValues = len(predictedList)
        if predictedValues == 0:
            return 1
        return correctValues / predictedValues

    def recall(self, predictedList, requiredList):
        """
        Helper Function

        Parameters:
        - predictedList = List of predicted tools/arguments/values
        - requiredList = List of required tools/arguments/values

        Returns:
        - Recall of the prediction
        """
        if isinstance(predictedList, list) == False and isinstance(requiredList, list) == False:
            if predictedList == requiredList:
                return 1
            else:
                return 0

        correctValues = len(self.correct_elements(predictedList, requiredList))
        requiredValues = len(requiredList)
        if requiredValues == 0:
            return 1
        return correctValues / requiredValues

    def f1_score(self, predictedList, requiredList):
        """
        Helper Function

        Parameters:
        - predictedList = List of predicted tools/arguments/values
        - requiredList = List of required tools/arguments/values

        Returns:
        - F1 Score of the prediction
        """
        if isinstance(predictedList, list) == False and isinstance(requiredList, list) == False:
            if predictedList == requiredList:
                return 1
            else:
                return 0

        precision = self.precision(predictedList, requiredList)
        recall = self.recall(predictedList, requiredList)
        return (2 * precision * recall)/(precision + recall)

    def find_tool_by_name(self, givenTools, toolName):
        """
        Helper Function

        Parameters:
        - givenTools = Given json of the tools and argument values
        - toolName = Name of the tool which we want to find

        Returns:
        - Tool description of the found tool
        - If not found, it returns {}
        """
        for tool in givenTools:
            if tool["tool_name"] == toolName:
                return tool
        return {}

    def find_arg_by_name(self, givenArgs, argName):
        """
        Helper Function

        Parameters:
        - givenArgs = Given json of the argument names and values
        - argName = Name of the argument which we want to find

        Returns:
        - Argument description of the found argument
        - If not found, it returns {}
        """
        for arg in givenArgs:
            if arg["argument_name"] == argName:
                return arg
        return {}

    def set_difference_operator(self, list1, list2):
        """
        Helper Function

        Parameters:
        - list1 = First list
        - list2 = Second list

        Returns:
        - The elements in the first list which are not present
        in the second list
        """
        return list(set(list1).difference(list2))

    def hallucination_tools(self, given_tool_names, predicted_tool_names):
        """
        Helper Function

        Parameters:
        - given_tool_names = Available tools names
        - predicted_tools = Tools predicted names

        Returns:
        - Hallucination rate on the predicted tools
        """
        hallucinated = list(set(predicted_tool_names).difference(given_tool_names))
        return len(hallucinated) / len(predicted_tool_names)

    def halluncination_args(self, given_arg_names, predicted_arg_names):
        """
        Helper Function

        Parameters:
        - given_arg_names = Available arguments names
        - predicted_arg_names = Predicted arguments names

        Returns:
        - Hallucination rate on the predicted arguments
        """
        hallucinated = list(set(predicted_arg_names).difference(given_arg_names))
        return len(hallucinated) / len(predicted_arg_names)

    def hallucination_rate(self, given_json, predicted_json):
        """
        Parameters:
        - given_json = Available tools and arguments description
        - predicted_json = Predicted tools and arguments

        Returns:
        - Overall hallucination rate
        """
        given_tool_names = self.get_tool_names(given_json)
        predicted_tool_names = self.get_tool_names(predicted_json)
        hallucination_rate_tools = self.hallucination_tools(given_tool_names, predicted_tool_names)

        predicted_args = []
        for tool in predictedJson:
            for arg in tool["arguments"]:
                predicted_args.append(tool["tool_name"]+arg["argument_name"])
        given_args = []
        for tool in givenJson:
            for arg in tool["arguments"]:
                given_args.append(tool["tool_name"]+arg["argument_name"])
        hallucination_rate_args = self.halluncination_args(given_args, predicted_args)

        return (hallucination_rate_tools + hallucination_rate_args) / 2

    def exactMatch(self, json1, json2):
        """
        Parameters:
        - json1 = First json object
        - json2 = Second json object

        Returns:
        - Boolean value which tells if the json1 and json2
          are exactly same or not
        """

        if len(json1) != len(json2):
            return False

        toolNames1 = self.get_tool_names(json1)
        toolNames2 = self.get_tool_names(json2)

        if toolNames1 != toolNames2:
            return False

        return self.ordered(json1) == self.ordered(json2)

    def f1_score_overall(self, predictedJson, requiredJson):
        """
        Parameters:
        - predictedJson = List of predicted json
        - requiredJson = List of required json

        Returns:
        - F1 Score of the prediction
        """
        predicted_tools = self.get_tool_descriptions(predictedJson)
        required_tools = self.get_tool_descriptions(requiredJson)
        predicted_tool_names = self.get_tool_names(predictedJson)
        required_tool_names = self.get_tool_names(requiredJson)

        f1_score_tools = self.f1_score(predicted_tool_names, required_tool_names)
        recall_tools = self.recall(predicted_tool_names, required_tool_names)

        correct_tool_names = self.correct_elements(predicted_tool_names, required_tool_names)

        f1_score_args_list = []
        recall_args_list = []
        f1_score_values_list = []
        recall_values_list = []
        for correct_tool_name in correct_tool_names:
            predicted_args = []
            predicted_args_names = []
            required_args = []
            required_args_names = []

            found_tool = self.find_tool_by_name(predicted_tools, correct_tool_name)
            if found_tool != {}:
                predicted_args = self.get_arguments(found_tool)
                predicted_args_names = self.get_arguments_names(found_tool)

            found_tool = self.find_tool_by_name(required_tools, correct_tool_name)
            if found_tool != {}:
                required_args = self.get_arguments(found_tool)
                required_args_names = self.get_arguments_names(found_tool)

            f1_score_tool_args = self.f1_score(predicted_args_names, required_args_names)
            f1_score_args_list.append(f1_score_tool_args)
            recall_tool_args = self.recall(predicted_args_names, required_args_names)
            recall_args_list.append(recall_tool_args)

            correct_arg_names = self.correct_elements(predicted_args_names, required_args_names)

            for correct_arg_name in correct_arg_names:
                predicted_values = []
                required_values = []

                found_arg = self.find_arg_by_name(predicted_args, correct_arg_name)
                if found_arg != {}:
                    predicted_values = found_arg["argument_value"]

                found_arg = self.find_arg_by_name(required_args, correct_arg_name)
                if found_arg != {}:
                    required_values = found_arg["argument_value"]

                f1_score_arg_values = self.f1_score(predicted_values, required_values)
                f1_score_values_list.append(f1_score_arg_values)
                recall_arg_values = self.recall(predicted_values, required_values)
                recall_values_list.append(recall_arg_values)

        f1_score_args = self.average(f1_score_args_list)
        f1_score_values = self.average(f1_score_values_list)
        recall_args = self.average(recall_args_list)
        recall_values = self.average(recall_values_list)

        w1 = 1
        w2 = recall_args
        w3 = recall_args * recall_values

        return ((w1 * f1_score_tools) + (w2 * f1_score_args) + (w3 * f1_score_values)) / (w1 + w2 + w3)
