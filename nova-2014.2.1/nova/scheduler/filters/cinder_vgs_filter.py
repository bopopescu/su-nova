# Copyright (c) 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from nova.openstack.common import log as logging
from nova.scheduler import filters

LOG = logging.getLogger(__name__)



class CinderDiskFilter(filters.BaseHostFilter):
    """Disk Filter with over subscription flag."""

    def host_passes(self, host_state, filter_properties):
        """Filter based on disk usage."""
        scheduler_hints = filter_properties.get('scheduler_hints') or {}
        requested_disk = int(scheduler_hints.get('vg_free', 0))
        if requested_disk == 0:
            return True;
        # if the node has cinder manager vg
        free_disk_gb = int(host_state.cinder_vgs_free)

        if not free_disk_gb >= requested_disk:
            LOG.info("%(host_state)s does not have %(requested_disk)s MB "
                    "usable disk, it only has %(free_disk_gb)s GB usable "
                    "disk.", {'host_state': host_state,
                               'requested_disk': requested_disk,
                               'free_disk_gb': free_disk_gb})
            return False

        return True
