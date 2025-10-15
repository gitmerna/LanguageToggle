# ToggleTranslatedUI は Interface で切り替えする為 operator が日本語に変換されなかった
# このアドオンは Interface を使わないので operator を日本語に変換できる

bl_info = {
    "name": "_ Z.Language Toggle",
    "author": "Yame",
    "version": (1, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Language Toggle",
    "description": "Toggle between saved language and English using a button (without using the user interface)",
    "category": "Interface",
}

import bpy
import bpy.app.translations as translations


# =========================================================
# アドオンのプリファレンス
# =========================================================
class LangTogglePreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    saved_language: bpy.props.StringProperty(
        name="Saved Language",
        default="",  # 初回は空
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "saved_language")


# =========================================================
# 言語切り替え関数
# =========================================================
def toggle_language():
    prefs = bpy.context.preferences
    addon_prefs = bpy.context.preferences.addons[__name__].preferences

    # 初回保存
    if not addon_prefs.saved_language:
        addon_prefs.saved_language = prefs.view.language

    current = prefs.view.language
    saved = addon_prefs.saved_language

    if current == saved:
        prefs.view.language = 'en_US'
    else:
        prefs.view.language = saved


# =========================================================
# オペレーター
# =========================================================
class LANGTOGGLE_OT_toggle(bpy.types.Operator):
    bl_idname = "wm.lang_toggle"
    bl_label = "Toggle Language"
    bl_description = "Toggle between saved language and English"

    def execute(self, context):
        toggle_language()
        self.report({'INFO'}, "Language toggled")
        return {'FINISHED'}


# =========================================================
# パネル
# =========================================================
class LANGTOGGLE_PT_panel(bpy.types.Panel):
    bl_label = "Language Toggle"
    bl_idname = "LANGTOGGLE_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        tr = bpy.app.translations.pgettext

        layout = self.layout
        layout.label(text="You can assign a shortcut")
        layout.label(text="from the right-click menu on the button")
        layout.operator(LANGTOGGLE_OT_toggle.bl_idname, text=tr("Toggle Language"), icon="FILE_REFRESH")


# ----------------------------------------------------
# 翻訳辞書
# ----------------------------------------------------
translation_dict = {
    "ja_JP": {
        ("*", "Language Toggle"): "言語切り替え機能",
        ("*", "Toggle Language"): "英語に切り替える",
        ("*", "You can assign a shortcut"): "ボタン上で右クリックメニューから",
        ("*", "from the right-click menu on the button"): "ショートカットを登録できます",
    },
}


# =========================================================
# 登録処理
# =========================================================
classes = (
    LangTogglePreferences,
    LANGTOGGLE_OT_toggle,
    LANGTOGGLE_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    translations.register(__name__, translation_dict)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    translations.unregister(__name__)


if __name__ == "__main__":
    register()
