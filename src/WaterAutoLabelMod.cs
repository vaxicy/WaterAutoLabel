using System.Collections.Generic;
using UnityEngine;

public sealed class WaterAutoLabelMod : IMod
{
    public const string AutoKey = "WaterAutoLabel.Enabled";
    private static ModLog _log;
    private static GameObject _ticker;
    private static bool _installed;

    public static bool AutoEnabled
    {
        get { return PlayerPrefs.GetInt(AutoKey, 1) == 1; }
        set { PlayerPrefs.SetInt(AutoKey, value ? 1 : 0); PlayerPrefs.Save(); }
    }

    public static void Log(string msg)
    {
        if (_log != null) _log.Log(msg);
        else Debug.Log("[WaterAutoLabel] " + msg);
    }

    public void Init(ModManifest manifest)
    {
        _log = new ModLog(manifest);
        Log("init");
    }

    public void OnEnable()
    {
        Install();
        Log("enabled");
    }

    public void OnDisable()
    {
        if (_ticker != null) UnityEngine.Object.Destroy(_ticker);
        _ticker = null;
        _installed = false;
        Log("disabled");
    }

    private void Install()
    {
        if (_installed) return;
        try
        {
            ModHelper.AddGameOptionSection("waterautolabel", "waterautolabel",
                () => ModHelper.GetLocalized("waterautolabel", "section_label"));
            ModHelper.AddGameOptionToggle("waterautolabel", "waterautolabel", "auto",
                () => ModHelper.GetLocalized("waterautolabel", "option_label"),
                () => AutoEnabled, v => AutoEnabled = v,
                () => ModHelper.GetLocalized("waterautolabel", "option_tooltip"));
        }
        catch (System.Exception e) { Log("options error: " + e.Message); }

        _ticker = new GameObject("WaterAutoLabelTicker");
        _ticker.AddComponent<WaterAutoLabelTicker>();
        UnityEngine.Object.DontDestroyOnLoad(_ticker);
        _installed = true;
    }
}

public sealed class WaterAutoLabelTicker : MonoBehaviour
{
    private float _next;
    private readonly Dictionary<GameItem, int> _lastPurity = new Dictionary<GameItem, int>();
    private int _cleanupFrame;

    private void Update()
    {
        if (!WaterAutoLabelMod.AutoEnabled) return;
        if (Time.unscaledTime < _next) return;
        _next = Time.unscaledTime + 0.5f;

        var inst = EmporiumEntry.Instance;
        if (inst == null) return;

        int updated = 0;
        foreach (var item in inst.GetAllOwnedItems(false, true))
        {
            if (item == null || !item.IsTag(WaterHelper.LIQUID_CONTAINER_TAG)) continue;

            int purity = WaterHelper.GetWaterPurity(item);
            int prev;
            if (_lastPurity.TryGetValue(item, out prev) && prev == purity) continue;

            _lastPurity[item] = purity;
            WaterFeatureHelper.OnLiquidChanged(item, true);
            updated++;
        }

        // 定期清理失效 item（避免缓存无限增长）
        if (Time.frameCount - _cleanupFrame > 3600)
        {
            _cleanupFrame = Time.frameCount;
            var dead = new List<GameItem>();
            foreach (var kv in _lastPurity) if (kv.Key == null) dead.Add(kv.Key);
            foreach (var k in dead) _lastPurity.Remove(k);
        }

        if (updated > 0) WaterAutoLabelMod.Log("auto-labeled " + updated + " water containers");
    }
}
