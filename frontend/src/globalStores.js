import { defineStore } from 'pinia'
import { api } from '../custom'


export const alertState = defineStore('alertState', 
{
    state: () => ({ 
        show: false,
        message: ''
    }),
})


export const tracklistState = defineStore('tracklistState', 
{
    state: () => ({ 
        tracklistExpanded: false,
    }),
})


export const uploadModalState = defineStore('uploadModalState', 
{
    state: () => ({ 
        uploadModalVisible: false,
    }),
})


export const userInfo = defineStore('userInfo', 
{
    state: () => ({ 
        username: '',
    }),
})

// export const trackInfo = defineStore('trackInfo', 
// {
//     state: () => ({ 
//         id: '',
//         trackname: '',
//         isTrackSelected: false,
//     }),

//     actions: {
//         getTrackList(){
//             api.get('http://127.0.0.1:5000/get-track-list')
//             .then((response) => {   

//                 // this.trackState[0].isTrackClicked = true
//                 response.data.forEach((oneTrack)=> {
//                     this.id = oneTrack.id
//                     this.trackname = oneTrack.trackname
//                 });
//             // currentTrackList.trackName = trackName
//             // currentTrackList.addToTrackList(response.data)
//             })
//         },
//     }
// })
 


export const trackList = defineStore('trackList', 
{
    state: () => ({ 
        trackState: [],
        // selectedTracks: [],
        barsList: [],
        midiList: []
    }),
    actions: {
       async fill(){
            await api.get('http://127.0.0.1:5000/get-track-list')
            .then((response) => {   
                this.trackState = response.data[0]
                this.barsList = response.data[1]
                this.midiList = response.data[2]

                // this.selectedTracks = []
                // response.data[0].forEach((oneTrack)=> {
                //     if(oneTrack.isTrackSelected == true){
                //         this.selectedTracks.push({trackName: oneTrack.trackName, id: oneTrack.id, isWaveform: oneTrack.isWaveform, isWaveformDisplayed: oneTrack.isWaveformDisplayed, isWaveformLoading: false})
                //     }
                    
                //     // this.selectedTracks.push({id: id++,trackName : oneTrack[0], isTrackSelected : oneTrack[1], isWaveform : oneTrack[2], wavesurfer : null})
                // });

            // currentTrackList.trackName = trackName
            // currentTrackList.addToTrackList(response.data)
            })
        },
        // addTrack(name) {
        //     this.trackState.push({id: 17, isTrackSelected: true, isWaveform: true, trackName: name })
        // }

    },
    
    getters: {
        
        selectTrack(state) {
            return (trackId) => state.trackState.find((track) => track.id == trackId)
        },
        // selectUsedTrack(state) {
        //     return (trackId) => state.selectedTracks.find((track) => track.id == trackId)
        // }
    }

})

export const trackIndex = defineStore('trackIndex', 
{
    state: () => ({ 
        selTrackIndex: '',
        selTracksToPlay: [],
    }),
})



