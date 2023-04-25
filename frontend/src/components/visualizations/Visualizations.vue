<script setup>
import ChartVisualization from "./charts/ChartVisualization.vue";
import Waveform from "./waveform/Waveform.vue";
import PianoRoll from "./pianoroll/PianoRoll.vue";
import Spectrogram from "./spectrogram/Spectrogram.vue";
import { trackIndex, trackList } from "../../stores/globalStores";

const currentTrackList = trackList()
const globalTrackIndex = trackIndex()

const getVisualizationProps = (track, intervalsType, type) => {
  const data = track[intervalsType + "_data"];
  return {
    id: track.id,
    trackName: track.trackName,
    graph_color: data.graph_color,
    graph_type: data.graph_type,
    txtFileName: track.txtFileName,
    showHorizontalAverage: data.showHorizontalAverage,
    showMovingAverage: data.showMovingAverage,
    movingAverageWindowSize: data.movingAverageWindowSize,
    histogramTimeFrameSize: data.histogramTimeFrameSize,
    histogramLengthFrameSize: data.histogramLengthFrameSize,
    height: data[intervalsType + "_dataHeight"],
    intervalsType: type,
    numOfFrames: data.numOfFrames,
  };
};
const emits = defineEmits(['selectVis'])
</script>



<template>

<div v-for="track in currentTrackList.trackState" :key="track.id" @click="globalTrackIndex.changeIndex(track.id)">
    <transition>
    <Waveform
        v-show="track.waveform.isWaveformDisplayed"
        :isSelected="track.id === globalTrackIndex.selTrackIndex"
        :track="track"
        @click="$emit('selectVis',0)"
    />
    </transition>
    <transition>
    <Spectrogram
        v-if="track.spectrogram.isSpectrogram && track.spectrogram.plotSpectrogram"
        v-show="track.spectrogram.isSpectrogramDisplayed"
        :isSelected="track.id === globalTrackIndex.selTrackIndex"
        :track="track"
        @click="$emit('selectVis',1)"

    />
    </transition>
    <transition>
    <PianoRoll
        v-if="track.pianoroll.isPianoroll"
        v-show="track.pianoroll.isPianorollDisplayed"
        :isSelected="track.id === globalTrackIndex.selTrackIndex"
        :track="track"
        @click="$emit('selectVis',2)"

    />
    </transition>

    <transition>
    <ChartVisualization
        v-if="track.imi_data.isIMI"
        v-show="track.imi_data.isIMIDisplayed"
        :isSelected="track.id === globalTrackIndex.selTrackIndex"
        :props="getVisualizationProps(track, 'imi', 'measure')"
        @click="$emit('selectVis',3)"

    />
    </transition>

    <transition>
    <ChartVisualization
        v-if="track.ioi_data.isIOI"
        v-show="track.ioi_data.isIOIDisplayed"
        :isSelected="track.id === globalTrackIndex.selTrackIndex"
        :props="getVisualizationProps(track, 'ioi', 'onset')"
        @click="$emit('selectVis',4)"

    />
    </transition>
    <transition>
    <ChartVisualization
        v-if="track.ibi_data.isIBI"
        v-show="track.ibi_data.isIBIDisplayed"
        :isSelected="track.id === globalTrackIndex.selTrackIndex"
        :props="getVisualizationProps(track, 'ibi', 'beats')"
        @click="$emit('selectVis',5)"

    />
    </transition>
    <transition>
    <ChartVisualization
        v-if="track.Tempo_data.isTempo"
        v-show="track.Tempo_data.isTempoDisplayed"
        :isSelected="track.id === globalTrackIndex.selTrackIndex"
        :props="getVisualizationProps(track, 'Tempo', 'Tempo')"
        @click="$emit('selectVis',6)"

    />
    </transition>
    <transition>
    <ChartVisualization
        v-if="track.RMS_data.isRMS"
        v-show="track.RMS_data.isRMSDisplayed"
        :isSelected="track.id === globalTrackIndex.selTrackIndex"
        :props="getVisualizationProps(track, 'RMS', 'RMS')"
        @click="$emit('selectVis',7)"

    />
    </transition>
</div>
</template>