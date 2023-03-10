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
        },
        changeState(id, propertyName, propertyValue) {
       
            const track = this.selectTrack(id)
            if (track) {
                const nestedProperties = propertyName.split('.');
                if (nestedProperties.length > 1) {
                  let nestedObject = track;
                  for (let i = 0; i < nestedProperties.length - 1; i++) {
                    nestedObject = nestedObject[nestedProperties[i]];
                  }
                  nestedObject[nestedProperties[nestedProperties.length - 1]] = propertyValue;
                } else {
                  track[propertyName] = propertyValue;
                }
            }
            
        },
    },

    
    getters: {       
        selectTrack: state => id => {
            
            return state.trackState.find(track => track.id === id)
        },
        // return (trackId) => state.trackState.find((track) => track.id == trackId)
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
    actions: {
        changeIndex(id) {
            this.selTrackIndex = id
        }
    }
})



