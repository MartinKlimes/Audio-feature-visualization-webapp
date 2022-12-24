import { defineStore } from 'pinia'

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
        trackName: '',
    }),
    // actions: {
    //     addToTrackList(trackList){
    //         this.trackName.push(trackList)
    //     }
    // }
})

export const trackIndex = defineStore('trackIndex', 
{
    state: () => ({ 
        selTrackIndex: '',
    }),
})


