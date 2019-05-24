#!/usr/bin/env python

# Copyright (c) 2018 Intel Labs.
# authors: German Ros (german.ros@intel.com)
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

""" This module implements an agent that roams around a track following random waypoints and avoiding other vehicles.
The agent also responds to traffic lights. """

from enum import Enum

import carla
from agents.navigation.agent import *
from agents.navigation.gut_local_planner import LocalPlanner
from agents.tools.misc import get_speed

class GUTAgent(Agent):
    """
    RoamingAgent implements a basic agent that navigates scenes making random
    choices when facing an intersection.

    This agent respects traffic lights and other vehicles.
    """

    def __init__(self, vehicle):
        """

        :param vehicle: actor to apply to local planner logic onto
        """
        super(GUTAgent, self).__init__(vehicle)
        self._proximity_threshold = 20.0  # meters
        self._state = AgentState.NAVIGATING
        self._local_planner = LocalPlanner(self._vehicle)
        self.recording = False

    def run_step(self, step, debug=False):
        """
        Execute one step of navigation.
        :return: carla.VehicleControl
        """

        # is there an obstacle in front of us?
        hazard_detected = False

        # retrieve relevant elements for safe navigation, i.e.: traffic lights
        # and other vehicles
        actor_list = self._world.get_actors()
        vehicle_list = actor_list.filter("*vehicle*")
        lights_list = actor_list.filter("*traffic_light*")
        limits_list = actor_list.filter("*speed_limit*")

        # # check possible obstacles
        # vehicle_state, vehicle = self._is_vehicle_hazard(vehicle_list)
        # if vehicle_state:
        #     if debug:
        #         print('!!! VEHICLE BLOCKING AHEAD [{}])'.format(vehicle.id))

        #     self._state = AgentState.BLOCKED_BY_VEHICLE
        #     hazard_detected = True

        # # check for the state of the traffic lights
        # is_red_light_ahead, traffic_light = self._is_light_red(lights_list)

        
        # if red_light_ahead:
        #     if debug:
        #         print('=== RED LIGHT AHEAD [{}])'.format(traffic_light.id))
        #     # TODO USE DISTANCE MEASUREMENT
        #     self._state = AgentState.BLOCKED_RED_LIGHT
        #     control.throttle = 0
        #     if speed > 5: 
        #         # brake if driving to fast
        #         brake = 0.8*(speed/30.0)
        #     else: 
        #         # fully brake if close to standing still            
        #         brake = 1.0
        #     # Don't stop on traffic lights
        #     # hazard_detected = True

        # speed_limit, sign = self._is_speed_limit(limits_list)
        # if light_state:
        #     if debug:
        #         print('=== SPEED SIGN AHEAD [{}])'.format(sign.id))
            # self._state = AgentState.BLOCKED_RED_LIGHT

        # if hazard_detected:
        #     control = self.emergency_stop()
        # else:
        self._state = AgentState.NAVIGATING
        # standard local planner behavior
        control = self._local_planner.run_step(step=step, recording=self.recording)
        # if is_red_light_ahead:
        #     # TODO TAKE DISTANCE INTO ACCOUNT!
        #     self._state = AgentState.BLOCKED_RED_LIGHT
        #     control.throttle = 0
        #     speed = get_speed(self._vehicle)
        #     if speed > 5: 
        #         # brake if driving to fast
        #         control.brake = 0.5*(speed/30.0)
        #     else: 
        #         # fully brake if close to standing still            
        #         control.brake = 1.0

        return control