from pycaw.pycaw import AudioUtilities
import numpy as np

class VolumeController:
    def __init__(self):
        device = AudioUtilities.GetSpeakers()
        self.volume = device.EndpointVolume
        
        volRange = self.volume.GetVolumeRange()
        self.minVol = volRange[0]
        self.maxVol = volRange[1]
        
    def set_volume(self, length, min_dist=15, max_dist=200):
        """
        Mapea la distancia en píxeles al rango de decibelios de Windows
        y aplica el volumen.
        """
        vol = np.interp(length, [min_dist, max_dist], [self.minVol, self.maxVol])
        
        volPercentage = np.interp(length, [min_dist, max_dist], [0, 100])
        
        self.volume.SetMasterVolumeLevel(vol, None)
        
        return volPercentage

    def get_current_volume_percentage(self):
        """Devuelve el volumen actual en formato porcentaje (0-100)"""
        current_vol = self.volume.GetMasterVolumeLevelScalar()
        return int(current_vol * 100)

if __name__ == "__main__":
    vc = VolumeController()
    print(f"Volumen actual: {vc.get_current_volume_percentage()}%")