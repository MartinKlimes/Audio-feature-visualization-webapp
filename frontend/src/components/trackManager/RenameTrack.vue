<script setup>
import { Icon } from "@iconify/vue";
import { ref, computed, reactive } from "vue";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength } from "@vuelidate/validators";
import { useI18n } from "vue-i18n";
import { api } from "../../../custom";
import { trackList } from "../../globalStores";
const { t, locale } = useI18n();

const currentTrackList = trackList();

const state = reactive({
  in_submission: false,
  showForm: false,
  showAlert: false,
  trackSelected: false,
  alert_variant: "",
  alert_message: "",
});

const props = defineProps({
  index: Number,
  name: String,
});

const emits = defineEmits(['deleteTrack'])

async function rename() {
  state.in_submission = true;
  state.showAlert = true;
  state.alert_variant = "bg-blue-500";
  state.alert_message = "Pleas wait";

  try {
    await api.get("/rename-track/" + props.name + "/" + modifiedName.value);
  } catch (error) {
    state.alert_variant = "bg-red-500";
    state.alert_message = "Something went wrong. Try again later";
    state.in_submission = false;
    return;
  }

  state.showAlert = true;
  state.alert_variant = "bg-green-500";
  state.alert_message = "Succesfuly renamed";
  state.in_submission = false;

  setTimeout(() => {
    currentTrackList.trackName[props.index] = modifiedName.value;
    state.showForm = false;
    state.showAlert = false;
  }, 1000);
}

const modifiedName = ref(props.name);
const requiredNameLength = ref(2);
const rules = computed(() => ({
  modifiedName: {
    required,
    minLength: minLength(requiredNameLength.value),
  },
}));

const v$ = useVuelidate(rules, { modifiedName });
const useTrack = () => {
  state.trackSelected = !state.trackSelected
}
</script>

<template>
  
  <div
  
    class="border border-gray-200 p-3 mb-4 rounded md:text-2xl cursor-pointer hover:bg-gray-100"
    :class="{ 'bg-gray-200 border-gray-400': state.showForm, 'bg-yellow-100 border-2 border-yellow-400 border-dashed shadow-md shadow-gray-400 hover:bg-yellow-100 ': state.trackSelected & !state.showForm}"
    
    @click="useTrack"
  >
    <div>
      <h4 class="inline-block font-bold">{{ name }}</h4>
      <button
      title="Delete song"
        class="ml-1 py-1 px-2 text-xs rounded text-white bg-red-600 float-right hover:bg-red-500"
        @click="$emit('deleteTrack', props)"
      >
        <Icon icon="fa:times" />
      </button>
      <button
        title="Rename song"
        class="ml-1 py-1 px-2 text-xs rounded text-white bg-green-600 hover:bg-green-500 float-right"
        @click="state.showForm = !state.showForm"
      >
        <Icon icon="fa:pencil" />
      </button>
    </div>
    <div v-show="state.showForm">
      <div
        v-if="state.showAlert"
        class="text-white text-center font-bold p-4 mb-4"
        :class="state.alert_variant"
      >
        {{ state.alert_message }}
      </div>

      <form>
        <div class="mb-3">
          <input
            type="text"
            class="block w-full py-1.5 px-3 text-gray-800 border border-gray-300 transition duration-500 focus:outline-none focus:border-black rounded"
            placeholder="Enter Song Title"
            v-model="v$.modifiedName.$model"
          />
          <div class="text-sm text-red-600 mb-1 mt-1">
            <span v-if="v$.modifiedName.$error">
              {{ t("edit-trackName") }}
            </span>
          </div>
        </div>

        <div v-if="!v$.modifiedName.$invalid">
          <button
            type="submit"
            class="py-1 px-2 rounded text-white bg-blue-600"
            @click.prevent="rename"
            :disabled="state.in_submission"
          >
            Submit
          </button>
        </div>
        <div v-else>
          <button
            type="submit"
            class="py-1 px-2 rounded text-white bg-gray-600"
            :disabled="v$.modifiedName.$invalid"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
