import { alertState } from './globalStores'

function showAlert(msg)
{
    const alertGlobalState = alertState();
    alertGlobalState.$patch({
        message: msg,
        show: true
    })
}

function closeAlert()
{
    const alertGlobalState = alertState();
    alertGlobalState.$patch({
        show: false,
        message: ''
    })
}

export {showAlert, closeAlert}