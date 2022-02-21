<template>
    <div class="body1">
        <div class="header">
            <h1 class="display3">Deployment status</h1>
            <a @click="updatePcsInDeploy()" href="#">
                <span class="material-icons"> refresh </span></a
            >
        </div>
        <div class="deploymentsContainer">
            <DeploymentStatus
                :deployment="pc"
                v-for="pc in pcsInDeploy"
                :key="pc.hostname"
            />
        </div>
    </div>
</template>

<script>
import DeploymentStatus from "./components/DeploymentStatus.vue";
import { ref } from "vue";
import "./assets/css/main.scss";
export default {
    name: "App",
    components: {
        DeploymentStatus,
    },
    setup: function () {
        const pcsInDeploy = ref([]);
        function updatePcsInDeploy() {
            fetch(process.env.VUE_APP_API || "" + "MDTMonitorEvent/deployments")
                .then((response) => response.json())
                .then((data) => {
                    pcsInDeploy.value = data;
                });
        }
        updatePcsInDeploy();
        setInterval(updatePcsInDeploy, 10000);
        return { pcsInDeploy, updatePcsInDeploy };
    },
};
</script>

<style></style>
