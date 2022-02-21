<template>
    <div
        class="deployment"
        :class="{
            error: deployment.error,
            complete: deployment.complete,
            stuck: isStuck && !(deployment.error || deployment.complete),
        }"
    >
        <div
            class="deploymentInner"
            :style="`background-size: ${
                (deployment.currentStep / deployment.totalSteps) * 100
            }%`"
        >
            <h2 class="headline5" style="margin: 0">
                {{ deployment.hostname }}
            </h2>
            <div v-if="!deployment.complete">
                Running step {{ deployment.currentStep }} out of
                {{ deployment.totalSteps }} - {{ deployment.stepName }}
            </div>
            {{ deployment.stepMessage }}
            <br />
            {{
                DateTime.fromSeconds(Math.round(deployment.stepTS)).toRelative()
            }}
            <br />
        </div>
    </div>
</template>

<script>
import { ref } from "vue";
import { DateTime } from "luxon";

export default {
    props: ["deployment"],
    setup: function (props) {
        const isStuck = ref(false);
        function updateStuck() {
            isStuck.value =
                Math.floor(Date.now() / 1000) - props.deployment.stepTS >
                60 * 5;
        }
        updateStuck();
        setInterval(updateStuck, 5000);
        return { isStuck, DateTime };
    },
};
</script>

<style></style>
