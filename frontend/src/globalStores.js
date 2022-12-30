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

export const trackInfo = defineStore('trackInfo', 
{
    state: () => ({ 
        fileNameList: '',
    }),
})

export const trackList = defineStore('trackList', 
{
    state: () => ({ 
        trackName: [],
    }),
    actions: {
        // addTrackList(trackList){
        //     this.trackName.push(trackList)
        // },
        getTrackList(){
            api.get('http://127.0.0.1:5000/get-track-list')
            .then((response) => {   
                this.trackName = []
                this.trackName.push(response.data) 
                
            // currentTrackList.trackName = trackName
            // currentTrackList.addToTrackList(response.data)
            })
        }
    }

})

export const trackIndex = defineStore('trackIndex', 
{
    state: () => ({ 
        selTrackIndex: '',
    }),
})


