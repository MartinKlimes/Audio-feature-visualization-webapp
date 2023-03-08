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
        async fetchRecordings() {
            try {
                const response = await api.get('/get-track-list')
                const recordings = response.data
               
                this.trackState = recordings[0]
                this.barsList = recordings[1]
                this.midiList = recordings[2]
              } catch (error) {
                console.error(error)
            }
        }
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



