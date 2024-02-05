import json
# from typing import Optional

import numpy as np


class Node:

    def __init__(self, wf: dict, id: int):

        # Read registered types of nodes and its inputs
        with open('./components/registered_nodes.json', 'r') as j:
            self.nodes_inputs_keys = json.load(j)

        self.node = self.get_node(wf, id)
        self.links = np.array([x[:5] for x in wf['links']])  # parse links without type of data
        self.id = str(self.node['id'])  # id must be str at comfyui api
        self.class_type = self.node['type']
        self.inputs = self.get_inputs()  # parse inputs

    def get_node(self, wf, id):
        # Find node by id

        for node in wf['nodes']:

            if node['id'] == id:
                return node

    def get_inputs(self):
        inputs = {}

        # Parse widget classes
        assert self.class_type in self.nodes_inputs_keys.keys(), f'"{self.class_type}" class_type is incorrect'
        keys = self.nodes_inputs_keys[self.class_type]

        if self.node.get('widgets_values'):
            assert len(keys) == len(self.node['widgets_values']), \
                f'number of keys does not match number of widgets_values: {keys}: {len(keys)} and {self.node["widgets_values"]}: {len(self.node["widgets_values"])}'

            for n, v in enumerate(self.node['widgets_values']):
                inputs[keys[n]] = v

        # Parse links
        if self.node.get('inputs'):

            for link in self.node['inputs']:
                link_id = link['link']
                name = link['name']

                in_node_id = self.links[self.links[:, 0] == link_id][0][1]
                in_slot_id = self.links[self.links[:, 0] == link_id][0][2]

                inputs[name] = [str(in_node_id), int(in_slot_id)]


class WorkFlow:

    def __init__(self, json_path: str):
        self.parsed_nodes = []
        self.json_path = json_path
        self.wf = self.read_workflow(json_path)
        self.skip_nodes = ['PreviewImage']  # a list of nodes that won't be used
        self.parsed_nodes = self.parse_nodes()

    def read_workflow(self, json_path):

        with open(json_path, 'r') as j:
            return json.load(j)

    def parse_nodes(self):

        for node in self.wf['nodes']:
            parsed_node = Node(wf=self.wf, id=node['id'])

            # Skip nodes
            if parsed_node.class_type in self.skip_nodes:
                continue

            self.parsed_nodes.append(parsed_node)

        return parsed_node

    def generate_prompt(self, save_path=None):
        # Generates the prompt for ComfyUI API
        prompt = dict()

        for node in self.parsed_nodes:
            prompt[node.id] = {
                'class_type': node.class_type,
                'inputs': node.inputs,
            }

        # Save to a file if save_path is provided
        if save_path:

            with open(save_path, 'w') as jdown:
                json.dump(prompt, jdown, sort_keys=True, ensure_ascii=False, indent=4)

        return prompt
