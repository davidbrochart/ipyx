// Copyright (c) David Brochart
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

export class XModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: XModel.model_name,
      _model_module: XModel.model_module,
      _model_module_version: XModel.model_module_version,
      _view_name: XModel.view_name,
      _view_module: XModel.view_module,
      _view_module_version: XModel.view_module_version,
      _value: 'None',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'XModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'XView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class XView extends DOMWidgetView {
  render() {
    this.el.classList.add('custom-widget');

    this.value_changed();
    this.model.on('change:_value', this.value_changed, this);
  }

  value_changed() {
    this.el.textContent = this.model.get('_value');
  }
}
